# POLYALPHABETIC (VIGENERE) CIPHER IMPLEMENTATION

def clean_text(text):
    return "".join([c.upper() for c in text if c.isalpha()])

# Convert A–Z → 0–25
def char_to_num(c):
    return ord(c) - ord('A')

# Convert 0–25 → A–Z
def num_to_char(n):
    return chr((n % 26) + ord('A'))

# -------------------- ENCRYPTION --------------------
def vigenere_encrypt(plaintext, key):
    plaintext = clean_text(plaintext)
    key = clean_text(key)

    ciphertext = ""
    key_length = len(key)

    for i, char in enumerate(plaintext):
        p = char_to_num(char)
        k = char_to_num(key[i % key_length])
        c = (p + k) % 26
        ciphertext += num_to_char(c)

    return ciphertext

# -------------------- DECRYPTION --------------------
def vigenere_decrypt(ciphertext, key):
    ciphertext = clean_text(ciphertext)
    key = clean_text(key)

    plaintext = ""
    key_length = len(key)

    for i, char in enumerate(ciphertext):
        c = char_to_num(char)
        k = char_to_num(key[i % key_length])
        p = (c - k) % 26
        plaintext += num_to_char(p)

    return plaintext

# -------------------- MAIN PROGRAM --------------------
print("=== POLY-ALPHABETIC CIPHER ===")

plaintext = input("Enter Plaintext   : ")
key = input("Enter Key         : ")

encrypted = vigenere_encrypt(plaintext, key)
decrypted = vigenere_decrypt(encrypted, key)

print("\n--- RESULTS ---")
print("Plaintext        :", plaintext)
print("Key              :", key.upper())
print("Encrypted Text   :", encrypted)
print("Decrypted Text   :", decrypted)
