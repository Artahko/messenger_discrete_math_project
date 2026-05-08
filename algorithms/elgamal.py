import random
import hashlib

p = 89884656743115795391714060562757515397425322659982333453951503557945186260897603074467021329267150667179270601498386514202185870349356296751727808353958732563710461587745543679948630665057517430779539542454135056582551841462788758130134369220761262066732236795930452718468922387238066961216943830683854773169
g = 2

def generate_keys(g, p):
    x = random.randint(2, p - 2)
    h = pow(g, x, p)
    return (x, h)

def text_to_int(text):
    return int(text.encode("utf-8").hex(), 16)

def int_to_text(num):
    h = hex(num)[2:]
    if len(h) % 2:
        h = "0" + h
    return bytes.fromhex(h).decode("utf-8", errors="replace")

def encrypt(message, h, g, p):
    """Encrypts a string or int message"""
    if isinstance(message, int):
        m = message
    else:
        m = text_to_int(message)
    if not (0 < m < p):
        return "Message too long for this key size"
    k = random.randint(2, p - 2)
    c1 = pow(g, k, p)
    c2 = (m * pow(h, k, p)) % p
    return (c1, c2)

def decrypt(c1, c2, x, p, as_int=False):
    """Decrypts ciphertext — returns int if as_int=True, else string"""
    s = pow(c1, x, p)
    m = (c2 * pow(s, -1, p)) % p
    if as_int:
        return m
    else:
        return int_to_text(m)


def sign(message, x, p, g):
    """Signs a string message with private key x"""
    h = int(hashlib.sha256(message.encode()).hexdigest(), 16) % (p - 1)
    while True:
        k = random.randint(2, p - 2)
        if __gcd(k, p - 1) == 1:
            break
    r = pow(g, k, p)
    k_inv = pow(k, -1, p - 1)
    s = (k_inv * (h - x * r)) % (p - 1)
    return (r, s)

def verify(message, r, s, h_pub, p, g):
    """Verifies ElGamal signature"""
    if not (0 < r < p):
        return False
    hm = int(hashlib.sha256(message.encode()).hexdigest(), 16) % (p - 1)
    lhs = pow(g, hm, p)
    rhs = (pow(h_pub, r, p) * pow(r, s, p)) % p
    return lhs == rhs

def __gcd(a, b):
    while b:
        a, b = b, a % b
    return a
