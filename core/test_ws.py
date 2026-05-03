import websocket
import json
import threading
from messenger.crypto.aes import AES
from messenger.crypto.rsa import AES
import base64
import os

TOKEN_USER_1 = "d3b413841747d1bdda21289319e772244a0d4052"
TOKEN_USER_2 = "966f4d8851638d82fe3a36f8ee034cbbed640273"
USER_2_ID = 2  # the ID of user 2

received_messages = []

stop_flag = threading.Event()

def listen(ws, label):
    aes = AES(aes_key)
    while not stop_flag.is_set():
        try:
            msg = ws.recv()
            if msg:
                data = json.loads(msg)

                if "ciphertext" in data and "encrypted_key" in data:

                    cipher_bytes = base64.b64decode(data["ciphertext"])
                    encrypted_key = base64.b64decode(data["encrypted_key"])

                    aes_key = rsa_decrypt(encrypted_key, my_private_key)

                    aes = AES(aes_key)
                    plaintext = aes.decrypt(cipher_bytes).decode()

                    print(f"[{label}] decrypted:", plaintext)
                else:
                    print(f"[{label}] received: {msg}")
                received_messages.append(msg)
        except Exception as e:
            if not stop_flag.is_set():
                print("Listener error:", e)
            break

# At the end, set flag before closing

aes_key = b"12312312312312311231231231231231"

# Connect both users
ws1 = websocket.WebSocket()
ws1.connect(f"ws://127.0.0.1:8000/ws/chat/?token={TOKEN_USER_1}")
print("User 1 connected")

ws2 = websocket.WebSocket()
ws2.connect(f"ws://127.0.0.1:8000/ws/chat/?token={TOKEN_USER_2}")
print("User 2 connected")

# Start listener thread for user 2
t = threading.Thread(target=listen, args=(ws2, "User 2"), daemon=True)
t.start()

# User 1 sends to user 2
aes = AES(aes_key)

cipher_bytes = aes.encrypt("hello from user 1")

cipher_b64 = base64.b64encode(cipher_bytes).decode()

ws1.send(json.dumps({
    "to": USER_2_ID,
    "ciphertext": cipher_b64
}))

# User 1 waits for confirmation
print("[User 1] received:", ws1.recv())

import time
time.sleep(1)  # give user 2 time to receive
stop_flag.set()

ws1.close()
ws2.close()
