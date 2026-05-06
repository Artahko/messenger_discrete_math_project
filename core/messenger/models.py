from django.db import models
from django.contrib.auth.models import User
import random

AVATARS = [
    "dru", "bob", "gru", "stuart_rose", "carl_megaphone",
    "kevin_hula", "kyle", "balthazar", "eduardo", "evil_minion",
    "stuart_unicorn", "jerry_music", "stuart_vampire", "scientist_minion", "gru_fairy",
    "lucy", "dr_nefario", "fritz", "bob_pajamas", "dave",
]

AVATAR_NAMES = {
    "dru": "Дру", "bob": "Боб", "gru": "Гру", "stuart_rose": "Стюарт з трояндою",
    "carl_megaphone": "Карл з мегафоном", "kevin_hula": "Кевін Хула", "kyle": "Кайл",
    "balthazar": "Бальтазар", "eduardo": "Едуардо", "evil_minion": "Злий міньйон",
    "stuart_unicorn": "Стюарт з єдинорогом", "jerry_music": "Джеррі з музикою",
    "stuart_vampire": "Стюарт-вампір", "scientist_minion": "Міньйон-вчений",
    "gru_fairy": "Гру-фея", "lucy": "Люсі", "dr_nefario": "Доктор Нефаріо",
    "fritz": "Фріц", "bob_pajamas": "Боб у піжамі", "dave": "Дейв",
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=32, unique=True)
    display_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=20, unique=True)
    avatar = models.CharField(max_length=32, default="bob")
    ecc_public_key_x = models.TextField(blank=True, null=True)
    ecc_public_key_y = models.TextField(blank=True, null=True)

    def set_public_key(self, Q):
        self.ecc_public_key_x = str(Q[0])
        self.ecc_public_key_y = str(Q[1])

    def get_public_key(self):
        if self.ecc_public_key_x and self.ecc_public_key_y:
            return (int(self.ecc_public_key_x), int(self.ecc_public_key_y))
        return None

    def __str__(self):
        return f"@{self.nickname} ({self.display_name})"


class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_by")

    class Meta:
        unique_together = ("owner", "contact")


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    ciphertext = models.TextField()
    file = models.FileField(upload_to="messages/%Y/%m/%d/", blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True)
    file_type = models.CharField(max_length=64, blank=True)
    rsa_signature = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Message({self.sender} -> {self.receiver}, {self.timestamp:%Y-%m-%d %H:%M})"
