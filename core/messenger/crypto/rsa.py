"""Module providing functions for RSA implementation"""

import random

def gcd(num1, num2):
    """Calculates greatecst common divisor of num1 and num2"""
    a = max(num1, num2)
    b = min(num1, num2)

    while b != 0:
        a, b = b, a % b

    return a

def pick_primes():
    """Picks 2 random prime numbers from file with large prime numbers prime_numbers.txt"""
    prime_numbers = []

    with open("prime_numbers.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip().split()
            prime_numbers.extend([int(el) for el in line])

    p = random.choice(prime_numbers)
    q = random.choice(prime_numbers)

    if p == q:
        return pick_primes()

    return (p, q)

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def mod_inverse(e, phi):
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise Exception("No modular inverse")
    return x % phi

def power(number, exponent, module):
    """Computes the power of a number raised to exponent with (mod module)"""
    result = 1
    number = number % module

    while exponent > 0:
        if exponent & 1:
            result = (result * number) % module
        number = (number * number) % module
        exponent = exponent // 2

    return result

def generate_keys():
    """
    Generates keys for RSA algorithm

    Uses pick_primes function to pick 'p' and 'q' as a base for the keys
    """
    p, q = pick_primes()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # standard choice

    if gcd(e, phi) != 1:
        raise Exception("e and phi not coprime")

    d = mod_inverse(e, phi)

    return (e, d, n)

def encrypt(m, e, n):
    """Encrypts message using public key (e, n) and returns encrypted cipher as string of numbers"""
    # Turn message into a list of numbers
    num_message = [ord(el) for el in m]
    cipher = [str(power(el, e, n)) for el in num_message]

    return " ".join(cipher)

def decrypt(c, d, n):
    """Decrypts cipher using private key (d, n) and returns decrypted message"""
    num_cipher = [int(el) for el in c.split()]
    message = [chr(power(el, d, n)) for el in num_cipher]

    # Assemble message back to a string
    return "".join(message)
