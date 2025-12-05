# ==========================================================
#   TRANSPOSITION TECHNIQUES IMPLEMENTATION
#   1. Rail Fence Cipher (Encrypt/Decrypt)
#   2. Columnar Transposition Cipher (Encrypt/Decrypt)
# ==========================================================

# -------------------- RAIL FENCE CIPHER --------------------

def rail_fence_encrypt(text, key):
    rail = ['' for _ in range(key)]
    row = 0
    direction = 1  # 1 = down, -1 = up

    for char in text.replace(" ", ""):
        rail[row] += char
        row += direction

        if row == key - 1 or row == 0:
            direction *= -1

    return "".join(rail)


def rail_fence_decrypt(cipher, key):
    # Determine zig-zag pattern
    pattern = [[] for _ in range(key)]
    row = 0
    direction = 1

    for _ in cipher:
        pattern[row].append('*')
        row += direction
        if row == key - 1 or row == 0:
            direction *= -1

    # Fill ciphertext in pattern
    index = 0
    for r in range(key):
        for i in range(len(pattern[r])):
            pattern[r][i] = cipher[index]
            index += 1

    # Read plaintext following zig-zag
    result = ""
    row = 0
    direction = 1

    for _ in cipher:
        result += pattern[row].pop(0)
        row += direction
        if row == key - 1 or row == 0:
            direction *= -1

    return result


# ---------------- COLUMNAR TRANSPOSITION CIPHER ----------------

def columnar_encrypt(text, key):
    text = text.replace(" ", "").upper()
    key = key.upper()

    # Determine order of columns
    order = sorted(list(key))
    col_order = {char: order.index(char) for char in key}

    # Create matrix
    cols = len(key)
    rows = (len(text) + cols - 1) // cols
    matrix = [['X' for _ in range(cols)] for _ in range(rows)]

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                matrix[r][c] = text[idx]
                idx += 1

    # Read column-wise in key order
    result = ""
    for char in order:
        col = key.index(char)
        for r in range(rows):
            result += matrix[r][col]

    return result


def columnar_decrypt(cipher, key):
    cipher = cipher.replace(" ", "").upper()
    key = key.upper()

    cols = len(key)
    rows = len(cipher) // cols

    # Column order
    order = sorted(list(key))
    col_idx = [order.index(k) for k in key]

    # Prepare empty matrix
    matrix = [['' for _ in range(cols)] for _ in range(rows)]

    # Fill cipher column-wise
    index = 0
    sorted_positions = sorted(range(cols), key=lambda x: key[x])

    for col in sorted_positions:
        for r in range(rows):
            matrix[r][col] = cipher[index]
            index += 1

    # Read row-wise to get plaintext
    result = ""
    for r in range(rows):
        for c in range(cols):
            result += matrix[r][c]

    return result


# -------------------- MAIN PROGRAM --------------------

print("=== Transposition Techniques ===")
print("1. Rail Fence Cipher")
print("2. Columnar Transposition Cipher")

choice = int(input("Choose (1/2): "))

if choice == 1:
    text = input("Enter text: ")
    key = int(input("Enter key (number of rails): "))

    enc = rail_fence_encrypt(text, key)
    dec = rail_fence_decrypt(enc, key)

    print("\n--- Rail Fence Cipher ---")
    print("Encrypted:", enc)
    print("Decrypted:", dec)

elif choice == 2:
    text = input("Enter text: ")
    key = input("Enter key (word): ")

    enc = columnar_encrypt(text, key)
    dec = columnar_decrypt(enc, key)

    print("\n--- Columnar Transposition Cipher ---")
    print("Encrypted:", enc)
    print("Decrypted:", dec)

else:
    print("Invalid choice!")
