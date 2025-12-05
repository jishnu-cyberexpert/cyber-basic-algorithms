from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
import binascii

# Convert bytes to readable hex
def to_hex(data):
    return binascii.hexlify(data).decode()


# -----------------------------
# AES ENCRYPTION
# -----------------------------
def aes_encrypt(plaintext, key, mode):
    plaintext = plaintext.encode()  # convert to bytes
    key = key.encode()              # key must be 16, 24, or 32 bytes

    if len(key) not in [16, 24, 32]:
        raise ValueError("AES key must be 16, 24, or 32 bytes.")

    # ---- MODE: ECB ----
    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        return ciphertext, None

    # ---- MODE: CBC ----
    elif mode == "CBC":
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        return ciphertext, iv

    # ---- MODE: CFB ----
    elif mode == "CFB":
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext, iv

    # ---- MODE: OFB ----
    elif mode == "OFB":
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_OFB, iv)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext, iv

    # ---- MODE: CTR ----
    elif mode == "CTR":
        nonce = get_random_bytes(8)
        ctr = Counter.new(64, prefix=nonce)
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext, nonce

    else:
        raise ValueError("Invalid AES Mode.")


# -----------------------------
# AES DECRYPTION
# -----------------------------
def aes_decrypt(ciphertext, key, mode, extra):
    key = key.encode()

    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()

    elif mode == "CBC":
        cipher = AES.new(key, AES.MODE_CBC, extra)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()

    elif mode == "CFB":
        cipher = AES.new(key, AES.MODE_CFB, extra)
        return cipher.decrypt(ciphertext).decode()

    elif mode == "OFB":
        cipher = AES.new(key, AES.MODE_OFB, extra)
        return cipher.decrypt(ciphertext).decode()

    elif mode == "CTR":
        ctr = Counter.new(64, prefix=extra)
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        return cipher.decrypt(ciphertext).decode()

    else:
        raise ValueError("Invalid Mode.")


# -----------------------------
# MAIN PROGRAM
# -----------------------------
print("\nAES MODES OF OPERATION DEMO\n")

plaintext = input("Enter plaintext: ")
key = input("Enter AES key (16/24/32 bytes): ")

print("\nSelect AES Mode:")
print("1. ECB")
print("2. CBC")
print("3. CFB")
print("4. OFB")
print("5. CTR")

choice = input("Enter choice: ")

modes = {"1": "ECB", "2": "CBC", "3": "CFB", "4": "OFB", "5": "CTR"}
mode = modes.get(choice)

ciphertext, extra = aes_encrypt(plaintext, key, mode)

print("\n--- Encryption Output ---")
print("Mode       :", mode)
print("Ciphertext :", to_hex(ciphertext))

if extra is not None:
    print("IV/Nonce   :", to_hex(extra))

print("\n--- Decryption Output ---")
print("Decrypted  :", aes_decrypt(ciphertext, key, mode, extra))
