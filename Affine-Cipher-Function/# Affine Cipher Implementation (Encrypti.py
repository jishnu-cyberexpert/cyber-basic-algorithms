import math

# -------------------------
# AFFINE CIPHER FUNCTIONS
# -------------------------
def clean_text(text):
    return "".join([c.upper() for c in text if c.isalpha()])

def char_to_num(c):
    return ord(c) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def validate_key(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        return False, "a and b must be integers."
    if math.gcd(a, 26) != 1:
        return False, "a must be coprime with 26 (gcd(a, 26) == 1)."
    if b < 0 or b > 25:
        return False, "b must be between 0 and 25."
    return True, "Valid key"

def affine_encrypt(plaintext, a, b):
    plaintext = clean_text(plaintext)
    cipher = ""
    for char in plaintext:
        p = char_to_num(char)
        c = (a * p + b) % 26
        cipher += num_to_char(c)
    return cipher

def affine_decrypt(ciphertext, a, b):
    ciphertext = clean_text(ciphertext)
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise ValueError("No modular inverse for a")
    plain = ""
    for char in ciphertext:
        c = char_to_num(char)
        p = (a_inv * (c - b)) % 26
        plain += num_to_char(p)
    return plain

# -------------------------
# USER INPUT SECTION
# -------------------------
print("----- Affine Cipher -----")

plaintext = input("Enter plaintext: ")

while True:
    try:
        a = int(input("Enter a (integer coprime with 26): "))
        b = int(input("Enter b (integer 0-25): "))
        valid, msg = validate_key(a, b)
        if valid:
            print("Key accepted!\n")
            break
        else:
            print("Invalid key:", msg)
    except ValueError:
        print("Please enter valid integers for a and b.")

encrypted = affine_encrypt(plaintext, a, b)
print("Encrypted:", encrypted)

decrypted = affine_decrypt(encrypted, a, b)
print("Decrypted:", decrypted)
