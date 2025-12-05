from Crypto.Hash import CMAC
from Crypto.Cipher import AES

def compute_cmac(key, message):
    cobj = CMAC.new(key, ciphermod=AES)
    cobj.update(message)
    return cobj.hexdigest()

# ----- USER INPUT -----
key_input = input("Enter 16-byte key (exactly 16 characters): ")
message_input = input("Enter message: ")

# Convert to bytes
key = key_input.encode()
message = message_input.encode()

# Validate key length
if len(key) != 16:
    print("Error: Key must be exactly 16 bytes (128-bit key for AES CMAC).")
    exit()

# ----- CMAC Calculation -----
cmac_value = compute_cmac(key, message)

# ----- OUTPUT -----
print("\n=== CMAC RESULT ===")
print("CMAC (AES-128):", cmac_value)
