from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=32, unique=True)        # унікальний нік
    display_name = models.CharField(max_length=64)                  # просто ім'я
    phone = models.CharField(max_length=20, unique=True)            # унікальний телефон
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
    """Хто кого додав у контакти."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_by")

    class Meta:
        unique_together = ("owner", "contact")

    def __str__(self):
        return f"{self.owner.profile.nickname} → {self.contact.profile.nickname}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    ciphertext = models.TextField()
    rsa_signature = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Message({self.sender} -> {self.receiver}, {self.timestamp:%Y-%m-%d %H:%M})"