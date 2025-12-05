# --------------------------------------------------------
#   ElGamal Key Exchange + Encryption/Decryption
#   Plain Python | No external libraries
# --------------------------------------------------------

import random

# Fast modular exponentiation
def power_mod(base, exp, mod):
    return pow(base, exp, mod)

# Modular inverse using Fermat's theorem (p must be prime)
def mod_inverse(a, p):
    return pow(a, p - 2, p)


# ------------------------------
# ElGamal Key Generation
# ------------------------------
def elgamal_keygen():
    p = int(input("Enter a large prime number p: "))
    g = int(input("Enter generator g: "))

    x = random.randint(2, p - 2)      # private key
    y = power_mod(g, x, p)            # public key

    print("\n--- Key Generation ---")
    print("Private key x =", x)
    print("Public key (p, g, y) = (", p, ",", g, ",", y, ")")

    return p, g, x, y


# ------------------------------
# ElGamal Encryption
# ------------------------------
def elgamal_encrypt(p, g, y, m):
    k = random.randint(2, p - 2)      # random session key

    c1 = power_mod(g, k, p)
    s  = power_mod(y, k, p)           # shared secret
    c2 = (m * s) % p

    print("\n--- Encryption ---")
    print("Random k =", k)
    print("Shared secret s =", s)
    print("Ciphertext: (c1, c2) = (", c1, ",", c2, ")")

    return c1, c2


# ------------------------------
# ElGamal Decryption
# ------------------------------
def elgamal_decrypt(p, x, c1, c2):
    s = power_mod(c1, x, p)           # shared secret

    s_inv = mod_inverse(s, p)
    m = (c2 * s_inv) % p

    print("\n--- Decryption ---")
    print("Shared secret s =", s)
    print("Inverse of s =", s_inv)
    print("Decrypted message m =", m)

    return m


# ------------------------------
# Main program
# ------------------------------
print("====== ElGamal Key Exchange + Encryption/Decryption ======\n")

p, g, x, y = elgamal_keygen()

m = int(input("\nEnter a message (as integer < p): "))
c1, c2 = elgamal_encrypt(p, g, y, m)

decrypted = elgamal_decrypt(p, x, c1, c2)

print("\nFinal Decrypted Message:", decrypted)
print("----------------------------------------------------------")
