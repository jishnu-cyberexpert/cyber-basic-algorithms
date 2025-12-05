# sha512_vs_code.py
# Pure-Python SHA-512 implementation + hashlib verification
# Ready to run in VS Code (Python 3.7+ recommended)

import struct
import hashlib

# 64-bit mask
MASK64 = (1 << 64) - 1

def rotr(x, n):
    """Right rotate for 64-bit words."""
    return ((x >> n) | ((x << (64 - n)) & MASK64)) & MASK64

def shr(x, n):
    return x >> n

# SHA-512 functions (big SIGMA / small sigma)
def big_sigma0(x):
    return (rotr(x, 28) ^ rotr(x, 34) ^ rotr(x, 39)) & MASK64

def big_sigma1(x):
    return (rotr(x, 14) ^ rotr(x, 18) ^ rotr(x, 41)) & MASK64

def small_sigma0(x):
    return (rotr(x, 1) ^ rotr(x, 8) ^ shr(x, 7)) & MASK64

def small_sigma1(x):
    return (rotr(x, 19) ^ rotr(x, 61) ^ shr(x, 6)) & MASK64

# SHA-512 constants (first 80 constant 64-bit words)
K = [
    0x428a2f98d728ae22, 0x7137449123ef65cd,
    0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
    0x3956c25bf348b538, 0x59f111f1b605d019,
    0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
    0xd807aa98a3030242, 0x12835b0145706fbe,
    0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
    0x72be5d74f27b896f, 0x80deb1fe3b1696b1,
    0x9bdc06a725c71235, 0xc19bf174cf692694,
    0xe49b69c19ef14ad2, 0xefbe4786384f25e3,
    0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
    0x2de92c6f592b0275, 0x4a7484aa6ea6e483,
    0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
    0x983e5152ee66dfab, 0xa831c66d2db43210,
    0xb00327c898fb213f, 0xbf597fc7beef0ee4,
    0xc6e00bf33da88fc2, 0xd5a79147930aa725,
    0x06ca6351e003826f, 0x142929670a0e6e70,
    0x27b70a8546d22ffc, 0x2e1b21385c26c926,
    0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
    0x650a73548baf63de, 0x766a0abb3c77b2a8,
    0x81c2c92e47edaee6, 0x92722c851482353b,
    0xa2bfe8a14cf10364, 0xa81a664bbc423001,
    0xc24b8b70d0f89791, 0xc76c51a30654be30,
    0xd192e819d6ef5218, 0xd69906245565a910,
    0xf40e35855771202a, 0x106aa07032bbd1b8,
    0x19a4c116b8d2d0c8, 0x1e376c085141ab53,
    0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
    0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb,
    0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
    0x748f82ee5defb2fc, 0x78a5636f43172f60,
    0x84c87814a1f0ab72, 0x8cc702081a6439ec,
    0x90befffa23631e28, 0xa4506cebde82bde9,
    0xbef9a3f7b2c67915, 0xc67178f2e372532b,
    0xca273eceea26619c, 0xd186b8c721c0c207,
    0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
    0x06f067aa72176fba, 0x0a637dc5a2c898a6,
    0x113f9804bef90dae, 0x1b710b35131c471b,
    0x28db77f523047d84, 0x32caab7b40c72493,
    0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
    0x4cc5d4becb3e42b6, 0x597f299cfc657e2a,
    0x5fcb6fab3ad6faec, 0x6c44198c4a475817
]

# Initial hash values for SHA-512
H0 = [
    0x6a09e667f3bcc908,
    0xbb67ae8584caa73b,
    0x3c6ef372fe94f82b,
    0xa54ff53a5f1d36f1,
    0x510e527fade682d1,
    0x9b05688c2b3e6c1f,
    0x1f83d9abfb41bd6b,
    0x5be0cd19137e2179
]

def sha512(data: bytes) -> str:
    """Compute SHA-512 digest of data (pure Python). Returns hex string."""
    # Pre-processing (padding)
    ml = len(data) * 8  # message length in bits (integer)
    # append the bit '1' (0x80), then k zero bytes, then 128-bit length (big-endian)
    data += b'\x80'
    # pad with zeros until message length ≡ 896 (mod 1024) -> i.e. length in bits ≡ 896 mod 1024
    # since we appended 1 byte (8 bits), check bytes length mod 128:
    while (len(data) * 8) % 1024 != 896:
        data += b'\x00'
    # append 128-bit big-endian message length (we place as two 64-bit words)
    # SHA-512 uses 128-bit length; for messages < 2^64 bits, high part is zero
    data += struct.pack('>QQ', 0, ml)  # big-endian two 64-bit words

    # Initialize working variables
    h = H0.copy()

    # Process the message in successive 1024-bit chunks (128 bytes)
    for chunk_offset in range(0, len(data), 128):
        chunk = data[chunk_offset:chunk_offset + 128]
        # Break chunk into 16 big-endian 64-bit words w[0..15]
        w = list(struct.unpack('>16Q', chunk))
        # Extend to 80 words
        for i in range(16, 80):
            s0 = small_sigma0(w[i - 15])
            s1 = small_sigma1(w[i - 2])
            val = (w[i - 16] + s0 + w[i - 7] + s1) & MASK64
            w.append(val)

        a, b, c, d, e, f, g, h_work = h  # unpack current hash state

        # Main compression loop
        for i in range(80):
            T1 = (h_work + big_sigma1(e) + ((e & f) ^ ((~e) & g)) + K[i] + w[i]) & MASK64
            T2 = (big_sigma0(a) + ((a & b) ^ (a & c) ^ (b & c))) & MASK64
            h_work = g
            g = f
            f = e
            e = (d + T1) & MASK64
            d = c
            c = b
            b = a
            a = (T1 + T2) & MASK64

        # Add the compressed chunk to the current hash value
        h = [
            (h[0] + a) & MASK64,
            (h[1] + b) & MASK64,
            (h[2] + c) & MASK64,
            (h[3] + d) & MASK64,
            (h[4] + e) & MASK64,
            (h[5] + f) & MASK64,
            (h[6] + g) & MASK64,
            (h[7] + h_work) & MASK64
        ]

    # Produce the final hash value (big-endian)
    return ''.join(f'{value:016x}' for value in h)


def hash_file_sha512_pure(path):
    """Compute SHA-512 of a file using the pure-Python sha512 function."""
    # For simplicity, read the whole file into memory (fine for small files).
    with open(path, 'rb') as f:
        data = f.read()
    return sha512(data)


def hash_file_sha512_hashlib(path):
    """Compute SHA-512 of a file using hashlib (streaming)."""
    hasher = hashlib.sha512()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def demo_interactive():
    print("SHA-512 (pure-Python) demo")
    print("-------------------------")
    choice = input("Hash (1) text or (2) file? Enter 1 or 2: ").strip()
    if choice == '1':
        txt = input("Enter text: ")
        b = txt.encode()
        p = sha512(b)
        lib = hashlib.sha512(b).hexdigest()
        print("\nPure-Python SHA-512:", p)
        print("hashlib SHA-512     :", lib)
        print("Match?              :", p == lib)
    elif choice == '2':
        path = input("Enter file path: ").strip()
        try:
            p = hash_file_sha512_pure(path)
            lib = hash_file_sha512_hashlib(path)
            print("\nPure-Python SHA-512:", p)
            print("hashlib SHA-512     :", lib)
            print("Match?              :", p == lib)
        except FileNotFoundError:
            print("File not found:", path)
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    demo_interactive()