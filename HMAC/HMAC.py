import hmac
import hashlib

# ----- USER INPUT -----
key = input("Enter Secret Key: ").encode()
message = input("Enter Message: ").encode()

# ----- HMAC CALCULATIONS -----
hmac_md5 = hmac.new(key, message, hashlib.md5).hexdigest()
hmac_sha1 = hmac.new(key, message, hashlib.sha1).hexdigest()
hmac_sha256 = hmac.new(key, message, hashlib.sha256).hexdigest()
hmac_sha512 = hmac.new(key, message, hashlib.sha512).hexdigest()

# ----- OUTPUT -----
print("\n=== HMAC RESULTS ===")
print("HMAC-MD5     :", hmac_md5)
print("HMAC-SHA1    :", hmac_sha1)
print("HMAC-SHA256  :", hmac_sha256)
print("HMAC-SHA512  :", hmac_sha512)
