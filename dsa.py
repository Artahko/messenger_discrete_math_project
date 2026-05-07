import hashlib
import random


def is_prime(n, k=10):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits):
    while True:
        n = random.getrandbits(bits) | (1 << bits - 1) | 1
        if is_prime(n):
            return n


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("inverse doesn't exist")
    return x % m


def hash_message(message):
    return int(hashlib.sha256(message.encode()).hexdigest(), 16)


def generate_keys(bits=256):
    q = generate_prime(bits)

    p_bits = bits * 4
    while True:
        k = random.getrandbits(p_bits - bits)
        p = k * q + 1
        if p.bit_length() >= p_bits and is_prime(p):
            break

    while True:
        h = random.randrange(2, p - 1)
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            break

    x = random.randrange(1, q)
    y = pow(g, x, p)

    public_key  = {"p": p, "q": q, "g": g, "y": y}
    private_key = {"p": p, "q": q, "g": g, "x": x}
    return public_key, private_key


def sign(message, private_key):
    p, q, g, x = private_key["p"], private_key["q"], private_key["g"], private_key["x"]
    H = hash_message(message) % q

    while True:
        k = random.randrange(1, q)
        r = pow(g, k, p) % q
        if r == 0:
            continue
        k_inv = mod_inverse(k, q)
        s = (k_inv * (H + x * r)) % q
        if s != 0:
            break

    return r, s


def verify(message, signature, public_key):
    p, q, g, y = public_key["p"], public_key["q"], public_key["g"], public_key["y"]
    r, s = signature

    if not (0 < r < q and 0 < s < q):
        return False

    H = hash_message(message) % q
    w = mod_inverse(s, q)
    u1 = (H * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q

    return v == r


def main():
    public_key, private_key = generate_keys(bits=256)

    message = "Hello, DSA!"
    r, s = sign(message, private_key)

    print(verify(message, (r, s), public_key))
    print(verify("змінене повідомлення", (r, s), public_key))


if __name__ == "__main__":
    main()