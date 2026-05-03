

import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer


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
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "user_group"):
            await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def receive(self, text_data):
        print(f"[DEBUG] receive() called with: {text_data}", flush=True)
        data = json.loads(text_data)
        receiver_id = data.get("to")
        ciphertext = data.get("ciphertext")  # ← read ciphertext instead of message

        # Confirm back to sender
        await self.send(text_data=json.dumps({
            "status": "sent",
            "to": receiver_id,
            "ciphertext": ciphertext,  # ← echo ciphertext back
        }))

        if receiver_id and ciphertext:
            await self.channel_layer.group_send(
                f"user_{int(receiver_id)}",
                {
                    "type": "chat.message",
                    "from": self.user.id,
                    "ciphertext": ciphertext,  # ← forward ciphertext
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "from": event["from"],
            "ciphertext": event["ciphertext"],  # ← send ciphertext to receiver
        }))
