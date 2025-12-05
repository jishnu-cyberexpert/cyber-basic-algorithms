# Elliptic Curve Diffie–Hellman (ECDH) Implementation

# Elliptic Curve Parameters
p = 37           # prime modulus
a = 0            # curve parameter 'a'
b = 7            # curve parameter 'b'

# Base point (generator)
G = (2, 7)


# Function: Modular Inverse (Extended Euclid)
def mod_inverse(k, p):
    return pow(k, p - 2, p)


# Function: Point Addition
def point_add(P, Q):
    if P == "O":
        return Q
    if Q == "O":
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 != y2:
        return "O"

    if P != Q:
        lam = ((y2 - y1) * mod_inverse((x2 - x1) % p, p)) % p
    else:  # Point Doubling
        lam = ((3 * x1 * x1 + a) * mod_inverse((2 * y1) % p, p)) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p

    return (x3, y3)


# Function: Scalar Multiplication (Double-and-Add)
def scalar_mult(k, P):
    result = "O"
    addend = P

    while k > 0:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result


# -------------------------
# ECDH Key Exchange
# -------------------------

print("Elliptic Curve Parameters:")
print(f"Curve: y^2 = x^3 + {a}x + {b} (mod {p})")
print("Generator Point G =", G)

# Alice chooses a private key 'a'
a_priv = int(input("\nAlice, enter your private key: "))
A_pub = scalar_mult(a_priv, G)
print("Alice's Public Key A = a*G =", A_pub)

# Bob chooses a private key 'b'
b_priv = int(input("\nBob, enter your private key: "))
B_pub = scalar_mult(b_priv, G)
print("Bob's Public Key B = b*G =", B_pub)

# Shared secret keys
S_A = scalar_mult(a_priv, B_pub)
S_B = scalar_mult(b_priv, A_pub)

print("\nShared Secret (Alice computes):", S_A)
print("Shared Secret (Bob computes):  ", S_B)

if S_A == S_B:
    print("\n✔ ECDH Successful! Shared secret =", S_A)
else:
    print("\n✘ Error: Secrets do not match!")
