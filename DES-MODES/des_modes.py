from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
import binascii

# Convert bytes to hex string
def to_hex(data):
    return binascii.hexlify(data).decode()

# DES encryption
def des_encrypt(plaintext, key, mode):
    plaintext = plaintext.encode()  # convert to bytes
    key = key.encode()              # key must be 8 bytes

    if len(key) != 8:
        raise ValueError("DES key must be exactly 8 bytes.")

    if mode == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(plaintext, 8))
        return ciphertext, None

    elif mode == "CBC":
        iv = get_random_bytes(8)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, 8))
        return ciphertext, iv

    elif mode == "CFB":
        iv = get_random_bytes(8)
        cipher = DES.new(key, DES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext, iv

    elif mode == "OFB":
        iv = get_random_bytes(8)
        cipher = DES.new(key, DES.MODE_OFB, iv)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext, iv

    elif mode == "CTR":
        nonce = get_random_bytes(4)
        ctr = Counter.new(32, prefix=nonce)
        cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext, nonce

    else:
        raise ValueError("Invalid mode selected.")

# DES decryption
def des_decrypt(ciphertext, key, mode, iv_or_nonce):
    key = key.encode()

    if mode == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
        plaintext = unpad(cipher.decrypt(ciphertext), 8)
        return plaintext.decode()

    elif mode == "CBC":
        cipher = DES.new(key, DES.MODE_CBC, iv_or_nonce)
        plaintext = unpad(cipher.decrypt(ciphertext), 8)
        return plaintext.decode()

    elif mode == "CFB":
        cipher = DES.new(key, DES.MODE_CFB, iv_or_nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode()

    elif mode == "OFB":
        cipher = DES.new(key, DES.MODE_OFB, iv_or_nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode()

    elif mode == "CTR":
        ctr = Counter.new(32, prefix=iv_or_nonce)
        cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode()

    else:
        raise ValueError("Invalid mode selected.")

# ---------------------------
# Main Program
# ---------------------------
print("\nDES MODES OF OPERATION DEMO\n")
plaintext = input("Enter plaintext: ")
key = input("Enter 8-byte key (example: mysecret): ")

print("\nSelect DES Mode:")
print("1. ECB")
print("2. CBC")
print("3. CFB")
print("4. OFB")
print("5. CTR")

choice = input("Enter choice: ")

modes = {"1": "ECB", "2": "CBC", "3": "CFB", "4": "OFB", "5": "CTR"}
mode = modes.get(choice)

ciphertext, extra = des_encrypt(plaintext, key, mode)

print("\n--- Encryption Output ---")
print("Mode       :", mode)
print("Ciphertext :", to_hex(ciphertext))

if extra is not None:
    print("IV/Nonce   :", to_hex(extra))

# Decryption
print("\n--- Decryption Output ---")
print("Decrypted  :", des_decrypt(ciphertext, key, mode, extra))
