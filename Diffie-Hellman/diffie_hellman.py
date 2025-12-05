# Diffie–Hellman Key Exchange Implementation

# Large prime number (p) and primitive root (g)
# For demo, using smaller numbers but in real systems values are very large
p = 23          # prime number
g = 5           # primitive root modulo p

print("Publicly known values:")
print("Prime (p):", p)
print("Primitive Root (g):", g)

# ---- Alice ----
a = int(input("Alice, enter your private key (a): "))
A = pow(g, a, p)   # g^a mod p
print("Alice's public key (A = g^a mod p):", A)

# ---- Bob ----
b = int(input("Bob, enter your private key (b): "))
B = pow(g, b, p)   # g^b mod p
print("Bob's public key (B = g^b mod p):", B)

# ---- Shared Secret Calculation ----
secret_A = pow(B, a, p)   # (g^b)^a mod p
secret_B = pow(A, b, p)   # (g^a)^b mod p

print("\nShared secret computed by Alice:", secret_A)
print("Shared secret computed by Bob:  ", secret_B)

# They must be equal
if secret_A == secret_B:
    print("\n✔ Key exchange successful! Shared secret key =", secret_A)
else:
    print("\n✘ Error: Keys do not match!")
