import random

p = 89884656743115795391714060562757515397425322659982333453951503557945186260897603074467021329267150667179270601498386514202185870349356296751727808353958732563710461587745543679948630665057517430779539542454135056582551841462788758130134369220761262066732236795930452718468922387238066961216943830683854773169
g = 2


def generate_keys(g, p):
    """Generates public h and private x keys"""
    x = random.randint(2, p - 2)
    h = pow(g, x, p)
    return x, h


def encrypt(message, h, g, p):
    """Encrypts a message using public key h and parameters g, p"""
    k = random.randint(2, p - 2)
    c1 = pow(g, k, p)
    c2 = (message * pow(h, k, p)) % p
    return c1, c2


def decrypt(c1, c2, x, p):
    """Decrypts ciphertext (c1, c2) using private key x"""
    s = pow(c1, x, p)
    return (c2 * pow(s, -1, p)) % p
