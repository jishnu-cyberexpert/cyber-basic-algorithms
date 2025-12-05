**AES Modes — README**

- **File**: `AES-Modes/aes_modes.py`: simple CLI demo that encrypts and decrypts text using AES in five modes (ECB, CBC, CFB, OFB, CTR).
- **Purpose**: Teach how AES modes differ, show required extra data (IV/nonce) for decryption, and demonstrate padding vs. stream modes.

**High-Level Flow**
- **Input**: user types a plaintext and a key (key length must be 16, 24, or 32 bytes).
- **Mode selection**: choose one of the five modes (ECB, CBC, CFB, OFB, CTR).
- **Encrypt**: `aes_encrypt(plaintext, key, mode)` returns a ciphertext and a mode-specific `extra` value (IV or nonce) or `None` for ECB.
- **Display**: prints ciphertext (hex) and IV/nonce (hex when present).
- **Decrypt**: `aes_decrypt(ciphertext, key, mode, extra)` uses the same key and `extra` to recover and print the plaintext.

**Key Functions Explained**
- **`to_hex(data)`**: converts bytes into a readable hex string using `binascii.hexlify`.
- **`aes_encrypt(plaintext, key, mode)`**:
  - Converts strings to bytes and validates key length (16/24/32).
  - ECB: `AES.MODE_ECB` — pads plaintext, returns `(ciphertext, None)`.
  - CBC: random 16-byte IV, pads plaintext, returns `(ciphertext, iv)`.
  - CFB / OFB: random 16-byte IV, treat AES like a stream cipher (no padding), return `(ciphertext, iv)`.
  - CTR: random 8-byte nonce used as counter prefix (`Counter.new(64, prefix=nonce)`), return `(ciphertext, nonce)`.
- **`aes_decrypt(ciphertext, key, mode, extra)`**:
  - Recreates the cipher with the same mode and `extra` (IV/nonce/counter), decrypts, unpads when needed, and returns the plaintext string.

**Mode-Specific Notes**
- **ECB**: deterministically encrypts blocks; identical plaintext blocks → identical ciphertext blocks. Not recommended for real data (pattern leakage).
- **CBC**: uses IV to randomize the first block. IV must be unpredictable; padding required.
- **CFB / OFB**: turn block cipher into stream ciphers; no padding, plaintext length preserved.
- **CTR**: stream-like and parallelizable; uses nonce + counter. NEVER reuse the same (key, nonce) pair.

**Important Implementation Details**
- **Padding**: `pad` / `unpad` are used for block-based modes (ECB, CBC) to align to AES block size (16 bytes).
- **Key validation**: the script raises an error if the key length is not 16/24/32 bytes.
- **IV / Nonce handling**: encryption returns IV/nonce; decryption requires the same value to restore plaintext.
- **Randomness**: `get_random_bytes` generates fresh IVs/nonces for each encryption (except ECB which has none).

**Security Considerations**
- **ECB insecurity**: avoid in production — use it only for demonstrations.
- **IV transmission**: IVs are not secret and are normally transmitted with the ciphertext, but they must be random/unpredictable for CBC.
- **Nonce reuse**: catastrophic for CTR — reusing a nonce with the same key leaks keystream.
- **Authentication missing**: the script lacks integrity checks or authentication (no MAC or AEAD). Prefer `AES-GCM` or use encrypt-then-MAC for real applications.

**How to Demo (quick)**
- Run the script:

```powershell
python .\AES-Modes\aes_modes.py
```

- Example inputs:
  - Plaintext: `Hello world`
  - Key: `thisisakey123456`  (16 bytes)
  - Mode: `2` (CBC)

- Show the printed ciphertext hex and IV hex, then the decryption output.
- For illustrating ECB weakness, encrypt a repeated-block plaintext like `"A"*32` and compare outputs for ECB vs CBC.

**Common Questions (short answers)**
- **Why pad?**: Block ciphers operate on fixed-size blocks; padding aligns the last block to 16 bytes.
- **Why CTR uses 8-byte nonce?**: This implementation uses a 64-bit counter; the nonce is the prefix. Implementations vary in nonce/counter sizing.
- **Can IV be sent in plaintext?**: Yes — IVs are typically sent alongside ciphertext. They must be random/unpredictable, not secret.
- **Why not use `AES-GCM`?**: `GCM` provides authenticated encryption (confidentiality + integrity) and is recommended for real use.

**Suggested Improvements**
- Add support for `AES.MODE_GCM` to provide authentication.
- Combine ciphertext and IV/nonce into a single serialized output (e.g., `nonce || ciphertext` or base64 container) for easier transport.
- Accept binary keys or derive keys from passphrases using KDFs like PBKDF2/scrypt.
- Improve error handling and provide clearer user messages for invalid inputs.
- Add unit tests for each mode and edge cases (wrong IV, wrong key, padding errors).

**Want me to also?**
- Add `GCM` support and an authenticated example.
- Update the script to output `nonce||ciphertext` in base64.
- Create a short slide or one-page summary for a quick demo.

If you'd like any of those, tell me which and I'll implement it.