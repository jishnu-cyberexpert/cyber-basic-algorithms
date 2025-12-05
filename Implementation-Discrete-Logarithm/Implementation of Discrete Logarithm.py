#!/usr/bin/env python3
"""
discrete_log.py

Solve discrete logarithm g^x ≡ h (mod p).

Provides:
 - brute_force_discrete_log
 - baby_step_giant_step (BSGS)

Author: ChatGPT
"""

import math
from collections import defaultdict

def modinv(a, m):
    """Modular inverse of a modulo m, returns None if inverse doesn't exist."""
    # Extended Euclid
    def egcd(a, b):
        if b == 0:
            return a, 1, 0
        g, x1, y1 = egcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

    g, x, _ = egcd(a % m, m)
    if g != 1:
        return None
    return x % m

def brute_force_discrete_log(g, h, p, limit=None):
    """
    Try all x from 0..limit-1 (or 0..p-2 by default) and return x if g^x ≡ h (mod p).
    Very slow for large p, but simple and useful for tiny examples.
    """
    if limit is None:
        limit = p - 1
    cur = 1
    for x in range(limit):
        if cur == h % p:
            return x
        cur = (cur * g) % p
    return None

def baby_step_giant_step(g, h, p):
    """
    Baby-step Giant-step algorithm to solve g^x ≡ h (mod p).
    Returns x if a solution exists; otherwise returns None.
    Works even if p is composite as long as g generates the subgroup containing h.
    Complexity: O(sqrt(n)) time and memory where n is the group order (≤ p).
    """
    g %= p
    h %= p
    if p == 1:
        return 0 if h == 0 else None

    # m = ceil(sqrt(n)). We don't always know group order; using m = ceil(sqrt(p)) is fine.
    m = math.isqrt(p) + 1

    # Baby steps: store g^{0..m-1} -> value to exponent mapping
    baby = {}
    baby_val = 1
    for j in range(m):
        # Only store the first occurrence (smallest j)
        if baby_val not in baby:
            baby[baby_val] = j
        baby_val = (baby_val * g) % p

    # Compute g^{-m} mod p
    gm = pow(g, m, p)
    gm_inv = modinv(gm, p)
    if gm_inv is None:
        # If gcd(gm, p) != 1, BSGS as-is cannot proceed; fall back or attempt variant.
        # We'll try a fallback naive search of multiples of m:
        # Try x = i*m + j for i from 0..m, j from baby dict
        # This fallback is expensive but handles some degenerate cases.
        for i in range(m + 1):
            # value = h * (g^(-m))^{i} not computable since inverse not exists
            # so we skip and fall back to brute force
            return brute_force_discrete_log(g, h, p)
    else:
        # Giant steps: look for collisions
        gamma = h
        for i in range(m):
            if gamma in baby:
                # x = i*m + j
                x = i * m + baby[gamma]
                # verify
                if pow(g, x, p) == h % p:
                    return x
            # multiply gamma by g^{-m}
            gamma = (gamma * gm_inv) % p

    return None

def solve_discrete_log(g, h, p, method='bsgs', brute_limit=1000000):
    """
    Solve discrete log using chosen method.
    method: 'bsgs' or 'brute'
    brute_limit: maximum exponent to try for brute-force
    """
    if method == 'brute':
        return brute_force_discrete_log(g, h, p, limit=brute_limit)
    elif method == 'bsgs':
        return baby_step_giant_step(g, h, p)
    else:
        raise ValueError("Unknown method: choose 'bsgs' or 'brute'")

def main():
    print("=== Discrete Logarithm Solver ===")
    print("Solve for x in: g^x ≡ h (mod p)\n")

    try:
        g = int(input("Enter base g (integer): ").strip())
        h = int(input("Enter value h (integer): ").strip())
        p = int(input("Enter modulus p (integer > 1): ").strip())
    except ValueError:
        print("Invalid integer input.")
        return

    if p <= 1:
        print("Modulus must be > 1.")
        return

    method = input("Method? (bsgs/brute) [default: bsgs]: ").strip().lower() or "bsgs"
    if method not in ('bsgs', 'brute'):
        print("Unknown method; using bsgs.")
        method = 'bsgs'

    # quick trivial checks
    g_mod = g % p
    h_mod = h % p

    if h_mod == 1:
        print("Trivial solution
