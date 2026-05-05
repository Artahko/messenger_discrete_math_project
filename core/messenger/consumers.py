import asyncio
import json
import base64
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message

logger = logging.getLogger(__name__)

active_users = {}
active_users_lock = asyncio.Lock()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.accept()
            await self.close(code=4001)
            return

        self.user_group = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.user_group, self.channel_name)

        async with active_users_lock:
            active_users[self.user.id] = self.channel_name

        await self.accept()
        logger.debug(f"[WS] {self.user.username} connected")

    async def disconnect(self, close_code):
        if hasattr(self, "user_group"):
            await self.channel_layer.group_discard(self.user_group, self.channel_name)

        async with active_users_lock:
            active_users.pop(self.user.id, None)

        logger.debug(f"[WS] {self.user.username} disconnected")

    async def receive(self, text_data):
        """
        Expected incoming JSON:
        {
            "to": <receiver_user_id>,
            "ciphertext": "<base64-encoded AES ciphertext>",
            "rsa_signature": "<base64-encoded RSA signature>"  (optional)
        }

        The ciphertext was produced by the sender's client:
            shared_key = ecc.calculate_shared_secret_key(Q_receiver, d_sender)
            aes = AES(shared_key)
            ciphertext = base64.b64encode(aes.encrypt(plaintext_message)).decode()
        """
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
            return

        receiver_id = data.get("to")
        ciphertext = data.get("ciphertext")
        rsa_signature = data.get("rsa_signature", "")

        if not receiver_id or not ciphertext:
            await self.send(text_data=json.dumps({"error": "Missing 'to' or 'ciphertext'"}))
            return

        # Persist encrypted message to DB
        await self.save_message(receiver_id, ciphertext, rsa_signature)

        # Echo back to sender as confirmation
        await self.send(text_data=json.dumps({
            "status": "sent",
            "to": receiver_id,
            "ciphertext": ciphertext,
            "rsa_signature": rsa_signature,
        }))

        # Forward to receiver's group
        await self.channel_layer.group_send(
            f"user_{int(receiver_id)}",
            {
                "type": "chat.message",
                "from": self.user.id,
                "from_username": self.user.username,
                "ciphertext": ciphertext,
                "rsa_signature": rsa_signature,
            }
        )

    async def chat_message(self, event):
        """Relay message to the WebSocket client."""
        await self.send(text_data=json.dumps({
            "from": event["from"],
            "from_username": event["from_username"],
            "ciphertext": event["ciphertext"],
            "rsa_signature": event.get("rsa_signature", ""),
        }))

    @sync_to_async
    def save_message(self, receiver_id, ciphertext, rsa_signature):
        """Persist encrypted message to the database."""
        from django.contrib.auth.models import User
        try:
            receiver = User.objects.get(id=receiver_id)
            Message.objects.create(
                sender=self.user,
                receiver=receiver,
                ciphertext=ciphertext,
                rsa_signature=rsa_signature or "",
            )
        except User.DoesNotExist:
            logger.warning(f"[WS] receiver {receiver_id} not found, message not saved")
