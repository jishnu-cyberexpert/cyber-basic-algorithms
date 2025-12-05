# CMAC — README

- File: `CMAC/CMAC.py` — CLI tool that computes an AES-CMAC tag for a user-supplied message.
- Purpose: demonstrate computing a message authentication code (CMAC) using AES-128 (PyCryptodome).

**High-level flow**
- Prompt user for a 16-byte key and a message.
- Convert inputs to bytes and validate key length.
- Compute the CMAC tag with `CMAC.new(key, ciphermod=AES)` and `cobj.update(message)`.
- Output the CMAC tag as a hexadecimal string.

**Key functions / lines explained**
- `from Crypto.Hash import CMAC` and `from Crypto.Cipher import AES` — import the CMAC helper and AES cipher from PyCryptodome.
- `compute_cmac(key, message)`:
  - Creates a CMAC object with `CMAC.new(key, ciphermod=AES)`.
  - Updates the object with `message` bytes using `cobj.update(message)`.
  - Returns a hex string of the tag using `cobj.hexdigest()`.
- Input handling:
  - `key_input = input(...)` / `message_input = input(...)` then `encode()` to bytes.
  - Key length validation: `if len(key) != 16:` ensures AES-128 key length.
- Output prints the computed CMAC tag labeled `CMAC (AES-128):`.

**What CMAC provides (and what it doesn't)**
- Provides: message authentication and integrity using a shared secret key.
- Does NOT provide: confidentiality — CMAC does not encrypt the message content.
- CMAC vs HMAC: CMAC uses a block cipher (AES); HMAC uses hash functions (SHA-family).

**Security & correctness notes**
- Keep the key secret and random. Do not type production keys interactively.
- The script requires exactly a 16-byte key (AES-128). Consider supporting 24/32-byte keys or deriving keys with a KDF (PBKDF2/scrypt) from passphrases.
- Use constant-time comparison or `cobj.verify(tag_bytes)` when verifying tags to avoid timing attacks.
- Avoid key reuse across different cryptographic purposes; use a KDF or key-derivation scheme if needed.
- Truncating tags reduces security; only truncate when protocol-level requirements justify it.

**How to demo (quick)**
- Run the script (PowerShell):

```powershell
python .\CMAC\CMAC.py
```

- Example inputs:
  - Key: `thisis16bytekey`  (exactly 16 characters)
  - Message: `Hello, CMAC!`
- Expected: prints a 32-character hex CMAC value (128-bit tag shown as hex).

**Quick verification example**
- To verify a received tag, recompute the CMAC with the shared key and compare in constant time, or use `cobj.verify(tag_bytes)` which raises an exception on mismatch.

**Common questions (short answers)**
- Q: Why exactly 16 bytes?  
  A: The script uses AES-128 (128-bit key). AES also supports 24/32 byte keys for AES-192/AES-256.
- Q: Is CMAC safe?  
  A: Yes for integrity/authentication when keys are managed correctly.
- Q: Can I use this to encrypt data?  
  A: No — CMAC authenticates only. Use AEAD (e.g., AES-GCM) or encrypt-then-MAC for confidentiality+integrity.

**Suggested improvements**
- Accept binary keys or derive keys from passphrases using PBKDF2/scrypt instead of requiring a 16-char input.
- Add a verification mode to accept a tag and validate it using `CMAC.verify`.
- Replace `exit()` with proper error handling and friendly messages.
- Add unit tests for compute + verify, different key sizes, and invalid inputs.
- For production use, integrate secure key management and consider AEAD (AES-GCM) when confidentiality and integrity are required.

**Next steps (optional)**
- I can add a verification mode to `CMAC.py`, implement KDF support, and add unit tests. Tell me which you want me to implement next.