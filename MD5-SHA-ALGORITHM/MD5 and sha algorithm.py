# ------------------------------------------------------------
# MD5 & SHA-1 Implementation in Python
# Python Program (Copy-Paste into VS Code → Save as hash_algorithms.py)
# Ready to run in VS Code
# ------------------------------------------------------------
import struct
import math


# ------------------------------------------------------------
# Helper: Left rotate
# ------------------------------------------------------------
def leftrotate(x, n, bits=32):
    x &= (2**bits - 1)
    return ((x << n) | (x >> (bits - n))) & (2**bits - 1)


# ------------------------------------------------------------
# MD5 Implementation
# ------------------------------------------------------------
def md5(data: bytes) -> str:
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    # K constants
    K = [int((1 << 32) * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

    # Rotation amounts
    s = (
        [7, 12, 17, 22] * 4 +
        [5, 9, 14, 20] * 4 +
        [4, 11, 16, 23] * 4 +
        [6, 10, 15, 21] * 4
    )

    # Padding
    original_len_bits = (len(data) * 8) & 0xffffffffffffffff
    data += b'\x80'
    while (len(data) * 8) % 512 != 448:
        data += b'\x00'

    data += struct.pack('<Q', original_len_bits)

    # Process in 512-bit chunks
    for chunk_offset in range(0, len(data), 64):
        chunk = data[chunk_offset:chunk_offset + 64]
        M = list(struct.unpack('<16I', chunk))

        a, b, c, d = A, B, C, D

        for i in range(64):
            if i < 16:
                f = (b & c) | (~b & d)
                g = i
            elif i < 32:
                f = (d & b) | (~d & c)
                g = (5*i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3*i + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7*i) % 16

            f = (f + a + K[i] + M[g]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + leftrotate(f, s[i])) & 0xFFFFFFFF

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    return ''.join(f"{x:02x}" for x in struct.pack('<4I', A, B, C, D))


# ------------------------------------------------------------
# SHA-1 Implementation
# ------------------------------------------------------------
def sha1(data: bytes) -> str:
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    original_len_bits = (len(data) * 8) & 0xffffffffffffffff
    data += b'\x80'
    while (len(data) * 8) % 512 != 448:
        data += b'\x00'

    data += struct.pack('>Q', original_len_bits)

    for chunk_offset in range(0, len(data), 64):
        chunk = data[chunk_offset:chunk_offset + 64]
        w = list(struct.unpack('>16I', chunk))

        for i in range(16, 80):
            w.append(leftrotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1))

        a, b, c, d, e = h0, h1, h2, h3, h4

        for i in range(80):
            if i < 20:
                f = (b & c) | (~b & d)
                k = 0x5A827999
            elif i < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif i < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (leftrotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
            e = d
            d = c
            c = leftrotate(b, 30)
            b = a
            a = temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    return f"{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}"


# ------------------------------------------------------------
# MAIN PROGRAM — user input for VS Code
# ------------------------------------------------------------
if __name__ == "__main__":
    print("\n--- MD5 & SHA-1 HASH GENERATOR ---\n")

    text = input("Enter your text: ")

    data = text.encode()

    print("\nMD5   : ", md5(data))
    print("SHA-1 : ", sha1(data))
    print("\nFinished.\n")