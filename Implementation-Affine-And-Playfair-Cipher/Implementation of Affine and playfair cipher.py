# ==========================================================
#   POLY-ALPHABETIC CIPHERS IMPLEMENTATION
#   1. Vigenère Cipher (Encrypt/Decrypt)
#   2. Auto-Key Cipher (Encrypt/Decrypt)
# ==========================================================

def clean_text(text):
    return "".join([c.upper() for c in text if c.isalpha()])

def char_to_num(c):
    return ord(c) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

# ------------------- VIGENERE ENCRYPT ----------------------
def vigenere_encrypt(plaintext, key):
    plaintext = clean_text(plaintext)
    key = clean_text(key)
    cipher = ""

    for i in range(len(plaintext)):
        p = char_to_num(plaintext[i])
        k = char_to_num(key[i % len(key)])
        cipher += num_to_char((p + k) % 26)

    return cipher


# ------------------- VIGENERE DECRYPT ----------------------
def vigenere_decrypt(ciphertext, key):
    ciphertext = clean_text(ciphertext)
    key = clean_text(key)
    plain = ""

    for i in range(len(ciphertext)):
        c = char_to_num(ciphertext[i])
        k = char_to_num(key[i % len(key)])
        plain += num_to_char((c - k) % 26)

    return plain


# ------------------- AUTO-KEY ENCRYPT ----------------------
def autokey_encrypt(plaintext, key):
    plaintext = clean_text(plaintext)
    key = clean_text(key) + plaintext  # append plaintext
    cipher = ""

    for i in range(len(plaintext)):
        p = char_to_num(plaintext[i])
        k = char_to_num(key[i])
        cipher += num_to_char((p + k) % 26)

    return cipher


# ------------------- AUTO-KEY DECRYPT ----------------------
def autokey_decrypt(ciphertext, key):
    ciphertext = clean_text(ciphertext)
    key = clean_text(key)
    plain = ""

    for i in range(len(ciphertext)):
        c = char_to_num(ciphertext[i])
        k = char_to_num(key[i])
        p = num_to_char((c - k) % 26)
        plain += p
        key += p  # append decrypted plaintext to key

    return plain


# -------------------------- MAIN --------------------------
print("=== POLY-ALPHABETIC CIPHERS ===")
print("1. Vigenère Cipher")
print("2. Auto-Key Cipher")

choice = int(input("Choose (1/2): "))

text = input("Enter Plaintext: ")
key = input("Enter Key: ")

if choice == 1:
    enc = vigenere_encrypt(text, key)
    dec = vigenere_decrypt(enc, key)

    print("\n--- VIGENÈRE RESULTS ---")
    print("Encrypted:", enc)
    print("Decrypted:", dec)

elif choice == 2:
    enc = autokey_encrypt(text, key)
    dec = autokey_decrypt(enc, key)

    print("\n--- AUTO-KEY RESULTS ---")
    print("Encrypted:", enc)
    print("Decrypted:", dec)

else:
    print("Invalid choice!")
