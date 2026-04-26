def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


def mod_sqrt_prime(c, p):
    return pow(c, (p + 1) // 4, p)


def generate_keys(p, q):
    assert is_prime(p), f"{p} is not prime"
    assert is_prime(q), f"{q} is not prime"
    assert p % 4 == 3, f"{p} must be 3 mod 4"
    assert q % 4 == 3, f"{q} must be 3 mod 4"
    return p * q, (p, q)


def encrypt(m, n):
    assert 0 <= m < n, "Message must be in range [0, n)"
    return (m * m) % n


def decrypt(c, p, q):
    n = p * q
    mp = mod_sqrt_prime(c, p)
    mq = mod_sqrt_prime(c, q)
    _, y_p, y_q = extended_gcd(p, q)
    r = (y_p * p * mq + y_q * q * mp) % n
    s = (y_p * p * mq - y_q * q * mp) % n
    return r, n - r, s, n - s


def text_to_int(text):
    return int(text.encode("utf-8").hex(), 16)


def int_to_text(num):
    h = hex(num)[2:]
    if len(h) % 2:
        h = "0" + h
    return bytes.fromhex(h).decode("utf-8", errors="replace")
