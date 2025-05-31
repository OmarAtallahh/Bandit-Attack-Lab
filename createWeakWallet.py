import hashlib
from eth_keys import keys
from eth_utils import to_checksum_address

password = input("Enter your password: ")

private_key_hex = hashlib.sha256(password.encode()).hexdigest()
priv_key_bytes = bytes.fromhex(private_key_hex)

private_key = keys.PrivateKey(priv_key_bytes)
public_key = private_key.public_key
address = to_checksum_address(public_key.to_address())

print("\n=== Wallet Generated ===")
print(f"Password       : {password}")
print(f"Private Key    : {private_key_hex}")
print(f"Public Address : {address}")
