# Elliptic Curve Arithmetic in Python (Affine Coordinates)
# Operations: Point Addition, Doubling, Scalar Multiplication
# Curve: y^2 = x^3 + a*x + b (mod p)
# Point at infinity is represented by None

# -----------------------------
# Extended Euclid (for inverse)
# -----------------------------
def extended_euclid(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_euclid(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a, p):
    a %= p
    g, x, _ = extended_euclid(a, p)
    if g != 1:
        return None
    return x % p

# -----------------------------
# ECC Operations
# -----------------------------
def is_on_curve(P, a, b, p):
    if P is None:
        return True
    x, y = P
    return (y * y - (x*x*x + a*x + b)) % p == 0

def point_neg(P, p):
    if P is None:
        return None
    x, y = P
    return (x, (-y) % p)

def point_add(P, Q, a, p):
    # If P is O
    if P is None:
        return Q
    # If Q is O
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = O
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P != Q:
        # slope = (y2 - y1) / (x2 - x1)
        inv = modinv((x2 - x1) % p, p)
        if inv is None:
            return None
        lam = ((y2 - y1) * inv) % p
    else:
        # Doubling: slope = (3*x1^2 + a) / (2*y1)
        if y1 % p == 0:
            return None
        inv = modinv((2 * y1) % p, p)
        lam = ((3 * x1 * x1 + a) * inv) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mul(k, P, a, p):
    result = None      # point at infinity
    addend = P

    while k > 0:
        if k & 1:  # if last bit is 1
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1  # shift right (divide by 2)

    return result

# -----------------------------
# Main Program
# -----------------------------
if __name__ == "__main__":
    print("Elliptic Curve Arithmetic Implementation")
    print("Curve: y^2 = x^3 + a*x + b (mod p)\n")

    a = int(input("Enter value of a: "))
    b = int(input("Enter value of b: "))
    p = int(input("Enter prime p: "))

    print("\n--- Base Point P ---")
    x = int(input("Enter x-coordinate of P: "))
    y = int(input("Enter y-coordinate of P: "))
    P = (x % p, y % p)

    if not is_on_curve(P, a, b, p):
        print("\nError: Point P is NOT on the curve. Exiting.")
        exit()

    print("\nPoint P is on the curve.\n")

    k = int(input("Enter scalar k for multiplication (k*P): "))

    R = scalar_mul(k, P, a, p)

    print("\nRESULT")
    print(f"k * P = {R}")
