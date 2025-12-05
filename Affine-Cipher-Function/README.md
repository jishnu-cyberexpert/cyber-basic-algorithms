# Affine Cipher Implementation

## Overview
The affine cipher is a substitution cipher that encrypts text using a linear mathematical formula. It combines multiplication and addition operations on character positions modulo 26.

## Affine Cipher Functions

### Utility Functions

#### `clean_text(text)`
Removes non-alphabetic characters and converts input to uppercase for processing.
- **Input:** Any text string
- **Output:** Uppercase alphabetic characters only

#### `char_to_num(c)`
Converts a character to its numeric position in the alphabet.
- **Mapping:** A=0, B=1, C=2, ..., Z=25
- **Input:** Single character
- **Output:** Integer (0-25)

#### `num_to_char(n)`
Converts a numeric position back to its corresponding character.
- **Input:** Integer value
- **Output:** Character (A-Z), handles wraparound with modulo 26

#### `mod_inverse(a, m)`
Finds the modular multiplicative inverse of `a` modulo `m`.
- **Purpose:** Essential for decryption (finding the inverse of the encryption key)
- **Input:** Integer `a` and modulus `m` (typically 26)
- **Output:** Integer that satisfies $(a \times \text{inverse}) \bmod m = 1$

#### `validate_key(a, b)`
Validates that the encryption keys meet requirements.
- **Validation Checks:**
  - `a` must be coprime with 26 (gcd(a, 26) = 1) to ensure decryption is possible
  - `b` must be between 0 and 25
  - Both must be integers
- **Input:** Keys `a` and `b`
- **Output:** Tuple of (valid: boolean, message: string)

### Encryption & Decryption Functions

#### `affine_encrypt(plaintext, a, b)`
Encrypts plaintext using the affine cipher formula.

**Formula:** 
$$c = (a \cdot p + b) \bmod 26$$

Where:
- `p` = numeric position of plaintext character
- `c` = numeric position of ciphertext character
- `a`, `b` = encryption keys

**Input:** Plaintext string, key `a` (coprime with 26), key `b` (0-25)  
**Output:** Encrypted string (uppercase, alphabetic only)

#### `affine_decrypt(ciphertext, a, b)`
Decrypts ciphertext back to plaintext using the inverse formula.

**Formula:**
$$p = a^{-1} \cdot (c - b) \bmod 26$$

Where:
- `c` = numeric position of ciphertext character
- `p` = numeric position of plaintext character
- $a^{-1}$ = modular multiplicative inverse of `a` modulo 26

**Input:** Ciphertext string, key `a`, key `b`  
**Output:** Decrypted plaintext string  
**Exception:** Raises `ValueError` if modular inverse cannot be found

## How It Works

### Example Encryption
**Plaintext:** "HELLO"  
**Keys:** a=5, b=8

| Char | Position | Calculation | Result | Encrypted |
|------|----------|-------------|--------|-----------|
| H    | 7        | (5×7+8)%26=9 | 9      | J         |
| E    | 4        | (5×4+8)%26=2 | 2      | C         |
| L    | 11       | (5×11+8)%26=11 | 11   | L         |
| L    | 11       | (5×11+8)%26=11 | 11   | L         |
| O    | 14       | (5×14+8)%26=0 | 0     | A         |

**Result:** "JCLLA"

### Key Requirements
- **a (multiplier):** Must be coprime with 26 (gcd = 1)
  - Valid values: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
- **b (shift):** Can be any value from 0 to 25

## Usage

```python
# Input plaintext
plaintext = "HELLO WORLD"

# Set keys (a must be coprime with 26)
a = 5  # coprime with 26
b = 8  # between 0-25

# Validate keys
valid, msg = validate_key(a, b)
if valid:
    # Encrypt
    encrypted = affine_encrypt(plaintext, a, b)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = affine_decrypt(encrypted, a, b)
    print(f"Decrypted: {decrypted}")
else:
    print(f"Invalid key: {msg}")
```

## Security Note
The affine cipher is a simple substitution cipher and is cryptographically weak. It has only 12 × 26 = 312 possible key combinations (12 valid values for `a`, 26 for `b`), making it vulnerable to brute-force attacks. It's suitable for educational purposes only, not for real security applications.
