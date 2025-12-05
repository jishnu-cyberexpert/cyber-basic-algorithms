# RSA Implementation with Fast Exponentiation and CRT Optimization

# -----------------------------------------------------------
# FAST MODULAR EXPONENTIATION (Exponentiation by Squaring)
# -----------------------------------------------------------
def fast_pow(base, exp, mod):
    result = 1
    base = base % mod

    while exp > 0:
        if exp % 2 == 1:        # If exponent is odd
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2               # floor division

    return result


# -----------------------------------------------------------
# EXTENDED EUCLID (for modular inverse)
# -----------------------------------------------------------
def extended_euclid(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_euclid(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inverse(a, m):
    g, x, y = extended_euclid(a, m)
    if g != 1:
        raise Exception("Inverse does not exist")
    return x % m


# -----------------------------------------------------------
# RSA KEY GENERATION
# -----------------------------------------------------------
def generate_keys():
    print("\n--- RSA Key Generation ---")
    p = int(input("Enter prime p: "))
    q = int(input("Enter prime q: "))

    n = p * q
    phi = (p - 1) * (q - 1)

    e = int(input("Enter e (public exponent, e < phi): "))

    d = mod_inverse(e, phi)

    print("\nPublic Key  : (e =", e, ", n =", n, ")")
    print("Private Key : (d =", d, ", n =", n, ")")

    return p, q, n, e, d


# -----------------------------------------------------------
# RSA DECRYPTION using CRT
# -----------------------------------------------------------
def rsa_decrypt_crt(c, p, q, d):
    print("\n--- CRT Based Decryption ---")

    # Step 1: Compute dp and dq
    dp = d % (p - 1)
    dq = d % (q - 1)

    # Step 2: Compute q inverse mod p
    q_inv = mod_inverse(q, p)

    # Step 3: Compute mp, mq
    mp = fast_pow(c, dp, p)
    mq = fast_pow(c, dq, q)

    # Step 4: Combine using CRT
    h = (q_inv * (mp - mq)) % p
    m = mq + h * q

    return m


# -----------------------------------------------------------
# MAIN PROGRAM
# -----------------------------------------------------------
if __name__ == "__main__":
    p, q, n, e, d = generate_keys()

    message = int(input("\nEnter numeric message m (< n): "))

    # Encrypt using fast exponentiation
    c = fast_pow(message, e, n)
    print("\nEncrypted Ciphertext =", c)

    # Decrypt using CRT
    decrypted = rsa_decrypt_crt(c, p, q, d)

    print("\nDecrypted Message =", decrypted)
