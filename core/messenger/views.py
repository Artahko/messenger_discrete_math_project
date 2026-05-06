import re
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser
from .models import UserProfile, Contact, Message, AVATARS, AVATAR_NAMES


def profile_data(profile):
    return {
        "user_id": profile.user_id,
        "nickname": profile.nickname,
        "display_name": profile.display_name,
        "phone": profile.phone,
        "avatar": profile.avatar,
    }


# auth
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    try:
        profile = request.user.profile
        return Response(profile_data(profile))
    except UserProfile.DoesNotExist:
        return Response({"user_id": request.user.id})


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    nickname     = request.data.get("nickname", "").strip()
    display_name = request.data.get("display_name", "").strip()
    phone        = request.data.get("phone", "").strip()
    password     = request.data.get("password", "")

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

    avatar = random.choice(AVATARS)
    user = User.objects.create_user(username=nickname.lower(), password=password)
    UserProfile.objects.create(
        user=user, nickname=nickname, display_name=display_name,
        phone=phone, avatar=avatar,
    )
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key, "user_id": user.id,
        "nickname": nickname, "display_name": display_name, "avatar": avatar,
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    login    = request.data.get("login", "").strip()
    password = request.data.get("password", "")

    if not login or not password:
        return Response({"error": "Введіть логін та пароль"}, status=400)

    try:
        if login.startswith("+") or login.isdigit():
            profile = UserProfile.objects.get(phone=login)
        else:
            profile = UserProfile.objects.get(nickname__iexact=login.lstrip("@"))
        user = authenticate(username=profile.user.username, password=password)
    except UserProfile.DoesNotExist:
        user = None

    if not user:
        return Response({"error": "Невірний логін або пароль"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key, "user_id": user.id,
        "nickname": profile.nickname, "display_name": profile.display_name,
        "avatar": profile.avatar,
    })


#account
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """DELETE /api/account/"""
    request.user.delete()
    return Response({"status": "deleted"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_avatar(request):
    """POST /api/account/avatar/"""
    avatar = request.data.get("avatar")
    if avatar not in AVATARS:
        return Response({"error": "Невірна аватарка"}, status=400)
    profile = request.user.profile
    profile.avatar = avatar
    profile.save()
    return Response({"avatar": avatar})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_avatars(request):
    """GET /api/avatars/"""
    return Response([{"id": a, "name": AVATAR_NAMES[a]} for a in AVATARS])


# ECC keys
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


# Contacts
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_user(request):
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
    contacts = Contact.objects.filter(owner=request.user).select_related("contact__profile")
    result = []
    for c in contacts:
        try:
            result.append(profile_data(c.contact.profile))
        except UserProfile.DoesNotExist:
            pass
    return Response(result)


#Messages

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
            "message_id": m.id if m.file else None,
            "file_name": m.file_name or None,
            "file_type": m.file_type or None,
            "timestamp": m.timestamp.isoformat(),
        })
    return Response(result)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_file(request, message_id):
    try:
        # only sender or receiver can download
        msg = Message.objects.get(
            id=message_id,
        )
    except Message.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.user != msg.sender and request.user != msg.receiver:
        return Response({"error": "Forbidden"}, status=403)

    import os
    from django.http import FileResponse
    if not msg.file:
        return Response({"error": "No file"}, status=404)

    return FileResponse(msg.file.open("rb"), content_type="application/octet-stream")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def send_file(request):
    receiver_id = request.data.get("to")
    file = request.FILES.get("file")

    if not receiver_id or not file:
        return Response({"error": "Missing 'to' or 'file'"}, status=400)

    from django.contrib.auth.models import User
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return Response({"error": "Receiver not found"}, status=404)

    # client sends original mime type separately since the uploaded blob is raw encrypted bytes
    file_type = request.data.get("file_type") or file.content_type
    file_name = request.data.get("file_name") or file.name

    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        file=file,
        file_name=file_name,
        file_type=file_type,
    )

    # Notify receiver via WebSocket that a file was sent
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{receiver_id}",
        {
            "type": "chat.message",
            "from": request.user.id,
            "from_username": request.user.username,
            "ciphertext": "",
            "message_id": message.id,
            "file_name": message.file_name,
            "file_type": message.file_type,
        }
    )

    return Response({
        "status": "sent",
        "message_id": message.id,
        "file_name": message.file_name,
        "file_type": message.file_type,
    })
