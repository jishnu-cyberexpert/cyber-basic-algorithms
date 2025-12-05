import numpy as np

# --- Function to convert character to number (A=0, B=1, ... Z=25)
def char_to_num(c):
    return ord(c) - ord('A')

# --- Function to convert number to character
def num_to_char(n):
    return chr((n % 26) + ord('A'))

# --- Function to clean plaintext/ciphertext
def clean_text(text):
    return "".join([c for c in text.upper() if c.isalpha()])

# --- Hill Cipher Encryption ---
def hill_encrypt(plaintext, key_matrix):
    plaintext = clean_text(plaintext)

    # Ensure even length (for 2x2 matrix)
    if len(plaintext) % 2 != 0:
        plaintext += "X"   # padding
    
    cipher_text = ""

    for i in range(0, len(plaintext), 2):
        block = np.array([[char_to_num(plaintext[i])],
                          [char_to_num(plaintext[i+1])]])
        
        result = np.dot(key_matrix, block) % 26

        cipher_text += num_to_char(result[0][0])
        cipher_text += num_to_char(result[1][0])

    return cipher_text


# --- Hill Cipher Decryption ---
def hill_decrypt(cipher_text, key_matrix):
    cipher_text = clean_text(cipher_text)
    
    # Compute inverse key matrix modulo 26
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = pow(det, -1, 26)  # modular inverse

    adj = np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
    inv_key = (det_inv * adj) % 26

    plain = ""

    for i in range(0, len(cipher_text), 2):
        block = np.array([[char_to_num(cipher_text[i])],
                          [char_to_num(cipher_text[i+1])]])

        result = np.dot(inv_key, block) % 26

        plain += num_to_char(result[0][0])
        plain += num_to_char(result[1][0])

    return plain


# ----------------- MAIN PROGRAM -----------------

print("=== HILL CIPHER PROGRAM ===")

# Key Matrix Input (2x2)
print("\nEnter 2x2 Key Matrix (only numbers):")
a = int(input("a11: "))
b = int(input("a12: "))
c = int(input("a21: "))
d = int(input("a22: "))

key_matrix = np.array([[a, b],
                       [c, d]])

plaintext = input("\nEnter Plaintext: ")

encrypted = hill_encrypt(plaintext, key_matrix)
decrypted = hill_decrypt(encrypted, key_matrix)

print("\n--- RESULTS ---")
print("Key Matrix:\n", key_matrix)
print("Encrypted Text :", encrypted)
print("Decrypted Text :", decrypted)
