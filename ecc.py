"""Module providing functions for ECC implementation"""

import random
import hashlib

# Elliptic curve parameters for secp256k1
a = 0
b = 7
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (Gx, Gy)

def add_point(P, Q, p):
    """Adds point Q to point P in module of p"""
    # Handle special cases when one point is the point of infinity
    if P is None:
        return Q
    if Q is None:
        return P

    # If points are equal then perform point doubling
    if P == Q:
        slope = (3 * P[0]**2 + a) * pow(2 * P[1], p - 2, p) % p
    # Else add two points together
    else:
        # Check if line is vertical
        if P[0] == Q[0] and P[1] != Q[1]:
            return

        slope = (Q[1] - P[1]) * pow(Q[0] - P[0], p - 2, p) % p

    x = (slope**2 - P[0] - Q[0]) % p
    y = (slope * (P[0]-x) - P[1]) % p

    return (x, y)

def point_multiply(k, P, p):
    """Multiplies point P to itself by k times using double-and-add algorithm"""
    R = None  # Initialize the result as the point at infinity
    Q = P

    while k:
        if k & 1:
            R = add_point(R, Q, p)  # Add Q to R if the current bit of k is 1

        Q = add_point(Q, Q, p) # Double the point Q
        k >>= 1  # Right-shift k to process the next bit

    return R

def generate_keys(G, n, p):
    """Generates public (G) and private (d) keys"""
    d = random.randint(1, n-1)
    Q = point_multiply(d, G, p)

    return d, Q

def keccak256(data):
    """Hashing function using Keccak-256"""
    return hashlib.sha3_256(data).digest()

def sign(message, private_key, G, n, p):
    """Signs a message using private_key and elliptic curve"""
    z_hex = keccak256(message).hex() # Hash the message to get z
    z = int(z_hex, 16) % n

    while True:
        k = random.randint(1, n - 1) # Generate random k for different signatures
        R = point_multiply(k, G, p)
        r = R[0] % n

        # Retry if r == 0
        if r == 0:
            continue

        # Calculate s = k^-1(z + r*d) mod n
        s = (pow(k, n - 2, n) * (z + r * private_key)) % n
        # Retry if s == 0
        if s == 0:
            continue

        break

    return (r, s), z_hex


def verify_sign(message, signature, public_key, G, n, p):
    """Verifies a signature using elliptic curve"""
    r, s = signature
    z_hex = keccak256(message).hex() # Hash the message to get z
    z = int(z_hex, 16) % n

    # Compute inverses
    w = pow(s, n - 2, n)
    u1 = (z * w) % n
    u2 = (r * w) % n

    # Calculate X = u1*G + u2*Q
    X = add_point(point_multiply(u1, G, p), point_multiply(u2, public_key, p), p)

    return r == X[0] % n, z_hex
