# crypto_algorithms.py
# Extended Euclid, Discrete Log (BSGS), Elliptic Curve Arithmetic
# Save & run in VS Code: python crypto_algorithms.py

import math
from collections import defaultdict

# -------------------------
# 1) EXTENDED EUCLID
# -------------------------
def extended_euclid(a, b):
    """
    Return (g, x, y) such that g = gcd(a, b) and a*x + b*y = g
    """
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0
    else:
        g, x1, y1 = extended_euclid(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

def modinv(a, m):
    """
    Modular inverse of a modulo m using Extended Euclid.
    Returns inverse in 0..m-1, or None if inverse does not exist.
    """
    a = a % m
    g, x, _ = extended_euclid(a, m)
    if g != 1:
        return None
    return x % m

# -------------------------
# 2) DISCRETE LOGARITHM
# -------------------------
def brute_force_discrete_log(g, h, p, limit=None):
    """
    Try all x from 0..limit-1 (or 0..p-2 by default) and return x such that g^x = h mod p.
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
    Solve g^x = h (mod p) using baby-step giant-step.
    Returns x or None if not found.
    """
    g %= p
    h %= p
    if p == 1:
        return 0 if h == 0 else None

    m = math.isqrt(p) + 1

    # Baby steps: store g^j -> j for j in [0, m-1]
    baby = {}
    baby_val = 1
    for j in range(m):
        if baby_val not in baby:
            baby[baby_val] = j
        baby_val = (baby_val * g) % p

    # Compute factor = g^{-m} mod p
    gm = pow(g, m, p)
    gm_inv = modinv(gm, p)
    if gm_inv is None:
        # Fallback: try brute force (degenerate case)
        return brute_force_discrete_log(g, h, p, limit=p-1)

    gamma = h
    for i in range(m):
        if gamma in baby:
            x = i * m + baby[gamma]
            if pow(g, x, p) == h % p:
                return x
        gamma = (gamma * gm_inv) % p

    return None

# -------------------------
# 3) ELLIPTIC CURVE ARITHMETIC (prime field)
# -------------------------
# We represent the point at infinity as None

def is_on_curve(P, a, b, p):
    """
    Check whether point P = (x, y) is on curve y^2 = x^3 + a*x + b (mod p).
    P = None is considered on the curve (point at infinity).
    """
    if P is None:
        return True
    x, y = P
    return (y * y - (x * x * x + a * x + b)) % p == 0

def point_neg(P, p):
    """Negation: -P for point P = (x, y) over F_p"""
    if P is None:
        return None
    x, y = P
    return (x, (-y) % p)

def point_add(P, Q, a, p):
    """
    Add points P and Q on curve with parameter a over field F_p.
    Returns R = P + Q.
    """
    # Handle special points
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % p == 0:
        # P + (-P) = O
        return None

    if P != Q:
        # slope = (y2 - y1) / (x2 - x1)
        denom = (x2 - x1) % p
        inv = modinv(denom, p)
        if inv is None:
            return None
        lam = ((y2 - y1) * inv) % p
    else:
        # P == Q -> doubling
        if y1 % p == 0:
            return None
        denom = (2 * y1) % p
        inv = modinv(denom, p)
        if inv is None:
            return None
        lam = ((3 * x1 * x1 + a) * inv) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mul(k, P, a, p):
    """
    Scalar multiplication k * P using double-and-add (left-to-right).
    k: non-negative integer
    """
    if k % p == 0 or P is None:
        return None
    if k < 0:
        return scalar_mul(-k, point_neg(P, p), a, p)

    R = None
    Q = P
    while k > 0:
        if k & 1:
            R = point_add(R, Q, a, p)
        Q = point_add(Q, Q, a, p)
        k >>= 1
    return R

# -------------------------
# DEMOS AND USAGE
# -------------------------
def demo_extended_euclid():
    print("Extended Euclid Demo")
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    g, x, y = extended_euclid(a, b)
    print(f"gcd({a},{b}) = {g}")
    print(f"Coefficients x = {x}, y = {y}")
    print(f"Verify: {a}*{x} + {b}*{y} = {a*x + b*y}")

    m = int(input("\nCompute modular inverse: Enter modulus m (for inverse of a mod m): "))
    inv = modinv(a, m)
    if inv is None:
        print(f"No inverse for {a} mod {m}")
    else:
        print(f"Inverse of {a} modulo {m} is {inv} (verify: {(a*inv) % m})")

def demo_discrete_log():
    print("Discrete Log Demo (solve g^x ≡ h mod p)")
    g = int(input("Enter base g: "))
    h = int(input("Enter h: "))
    p = int(input("Enter modulus p (>1): "))
    method = input("Method (bsgs/brute) [bsgs]: ").strip().lower() or "bsgs"
    if method not in ("bsgs", "brute"):
        method = "bsgs"
    if method == "brute":
        x = brute_force_discrete_log(g, h, p)
    else:
        x = baby_step_giant_step(g, h, p)
    if x is None:
        print("No solution found (or not within search limits).")
    else:
        print(f"Solution x = {x}")
        print(f"Verify: {pow(g, x, p)} == {h % p}")

def demo_ecc():
    print("Elliptic Curve Arithmetic Demo (Prime field)")
    print("Curve: y^2 = x^3 + a*x + b (mod p)")
    a = int(input("Enter curve parameter a: "))
    b = int(input("Enter curve parameter b: "))
    p = int(input("Enter prime modulus p: "))

    print("\nEnter base point P (x,y) or leave x blank for point at infinity.")
    x_in = input("x (or blank): ").strip()
    if x_in == "":
        P = None
    else:
        xP = int(x_in)
        yP = int(input("y: "))
        P = (xP % p, yP % p)

    if not is_on_curve(P, a, b, p):
        print("Warning: The provided point P is NOT on the curve with given parameters.")
    else:
        print("Point P is on the curve.")

    # operations
    if P is None:
        print("Point at infinity selected; scalar multiples are point at infinity.")
    else:
        k = int(input("Enter scalar k to compute k*P: "))
        R = scalar_mul(k, P, a, p)
        print(f"{k} * P = {R}")

        # demonstration of addition/doubling
        Q = P
        S = point_add(P, Q, a, p)
        print(f"P + P = {S} (should equal 2*P)")

        # verify associativity sample ( (P+P)+P == P+(P+P) )
        left = point_add(point_add(P, P, a, p), P, a, p)
        right = point_add(P, point_add(P, P, a, p), a, p)
        print("Associativity check (P+P)+P == P+(P+P):", left == right)

# -------------------------
# MAIN MENU
# -------------------------
def main():
    print("Crypto Algorithms Collection")
    print("1) Extended Euclid")
    print("2) Discrete Logarithm (BSGS & brute)")
    print("3) Elliptic Curve Arithmetic (prime field)")
    choice = input("Choose demo (1/2/3) or press Enter to run examples: ").strip()

    if choice == "1":
        demo_extended_euclid()
    elif choice == "2":
        demo_discrete_log()
    elif choice == "3":
        demo_ecc()
    else:
        # Run small examples
        print("\nRunning small examples...\n")
        # Extended Euclid example
        print("Extended Euclid: gcd(30, 50)")
        g, x, y = extended_euclid(30, 50)
        print("gcd =", g, "coefficients:", x, y, "verify:", 30*x + 50*y)

        # Discrete log example
        print("\nDiscrete log example: solve 5^x ≡ 8 (mod 23) (expected x=6)")
        x = baby_step_giant_step(5, 8, 23)
        print("Found x =", x)

        # ECC example: curve y^2 = x^3 + 2x + 3 mod 97, base point (3,6)
        print("\nECC example: curve y^2 = x^3 + 2x + 3 (mod 97), P=(3,6)")
        a, b, p = 2, 3, 97
        P = (3, 6)
        print("P on curve?", is_on_curve(P, a, b, p))
        print("2P =", scalar_mul(2, P, a, p))
        print("3P =", scalar_mul(3, P, a, p))

if __name__ == "__main__":
    main()