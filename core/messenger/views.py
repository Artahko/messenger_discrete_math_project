import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import UserProfile, Contact, Message


# ── helpers ───────────────────────────────────────────────────────────────────

def profile_data(profile):
    return {
        "user_id": profile.user_id,
        "nickname": profile.nickname,
        "display_name": profile.display_name,
        "phone": profile.phone,
    }


# ── Auth ──────────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    POST /api/register/
    Body: { nickname, display_name, phone, password }
    """
    nickname     = request.data.get("nickname", "").strip()
    display_name = request.data.get("display_name", "").strip()
    phone        = request.data.get("phone", "").strip()
    password     = request.data.get("password", "")

    # ── validation ────────────────────────────────────────────────────────────
    errors = {}

    if not nickname:
        errors["nickname"] = "Нікнейм обовʼязковий"
    elif not re.match(r'^[a-zA-Z0-9_]{3,32}$', nickname):
        errors["nickname"] = "Нікнейм: 3–32 символи, лише латиниця, цифри та _"
    elif UserProfile.objects.filter(nickname__iexact=nickname).exists():
        errors["nickname"] = "Цей нікнейм вже зайнятий"

    if not display_name:
        errors["display_name"] = "Імʼя обовʼязкове"

    if not phone:
        errors["phone"] = "Телефон обовʼязковий"
    elif not re.match(r'^\+?\d{7,15}$', phone):
        errors["phone"] = "Невірний формат телефону"
    elif UserProfile.objects.filter(phone=phone).exists():
        errors["phone"] = "Цей номер вже зареєстрований"

    if len(password) < 6:
        errors["password"] = "Пароль мінімум 6 символів"

    if errors:
        return Response({"errors": errors}, status=400)

    # ── create ────────────────────────────────────────────────────────────────
    user = User.objects.create_user(username=nickname.lower(), password=password)
    UserProfile.objects.create(
        user=user,
        nickname=nickname,
        display_name=display_name,
        phone=phone,
    )
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "user_id": user.id,
        "nickname": nickname,
        "display_name": display_name,
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    POST /api/login/
    Body: { login, password }  — login = нік або телефон
    """
    login    = request.data.get("login", "").strip()
    password = request.data.get("password", "")

    if not login or not password:
        return Response({"error": "Введіть логін та пароль"}, status=400)

    # знайти профіль по ніку або телефону
    try:
        if login.startswith("+") or login.isdigit():
            profile = UserProfile.objects.get(phone=login)
        else:
            profile = UserProfile.objects.get(nickname__iexact=login)
        user = authenticate(username=profile.user.username, password=password)
    except UserProfile.DoesNotExist:
        user = None

    if not user:
        return Response({"error": "Невірний логін або пароль"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "user_id": user.id,
        "nickname": profile.nickname,
        "display_name": profile.display_name,
    })


# ── ECC keys ──────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_public_key(request):
    x = request.data.get("x")
    y = request.data.get("y")
    if not x or not y:
        return Response({"error": "x and y required"}, status=400)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.set_public_key((int(x), int(y)))
    profile.save()
    return Response({"status": "ok"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_public_key(request, user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    Q = profile.get_public_key()
    if not Q:
        return Response({"error": "No key yet"}, status=404)
    return Response({"user_id": user_id, "x": str(Q[0]), "y": str(Q[1])})


# ── Contacts ──────────────────────────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_user(request):
    """
    GET /api/search/?q=<нік або телефон>
    Шукає користувача по ніку або телефону.
    """
    q = request.GET.get("q", "").strip()
    if not q:
        return Response({"error": "Введіть нік або номер"}, status=400)

    try:
        if q.startswith("+") or q.isdigit():
            profile = UserProfile.objects.get(phone=q)
        else:
            profile = UserProfile.objects.get(nickname__iexact=q.lstrip("@"))
    except UserProfile.DoesNotExist:
        return Response({"found": False})

    if profile.user_id == request.user.id:
        return Response({"found": False, "error": "Це ви самі"})

    already = Contact.objects.filter(owner=request.user, contact=profile.user).exists()
    return Response({"found": True, "already_contact": already, **profile_data(profile)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_contact(request):
    """
    POST /api/contacts/add/
    Body: { user_id }
    """
    uid = request.data.get("user_id")
    if not uid:
        return Response({"error": "user_id required"}, status=400)
    try:
        target = User.objects.get(id=uid)
    except User.DoesNotExist:
        return Response({"error": "Користувача не знайдено"}, status=404)

    if target == request.user:
        return Response({"error": "Не можна додати себе"}, status=400)

    Contact.objects.get_or_create(owner=request.user, contact=target)
    return Response({"status": "ok"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_contacts(request):
    """GET /api/contacts/ — список контактів поточного юзера."""
    contacts = Contact.objects.filter(owner=request.user).select_related("contact__profile")
    result = []
    for c in contacts:
        try:
            result.append(profile_data(c.contact.profile))
        except UserProfile.DoesNotExist:
            pass
    return Response(result)


# ── Messages ──────────────────────────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def message_history(request, user_id):
    messages = (
        Message.objects.filter(sender=request.user, receiver_id=user_id) |
        Message.objects.filter(sender_id=user_id, receiver=request.user)
    )
    result = []
    for m in messages.order_by("timestamp"):
        result.append({
            "id": m.id,
            "from": m.sender_id,
            "to": m.receiver_id,
            "ciphertext": m.ciphertext,
            "rsa_signature": m.rsa_signature,
            "timestamp": m.timestamp.isoformat(),
        })
    return Response(result)