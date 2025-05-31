import requests
import time
import sys
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

# Configuration
TARGET_BALANCE_THRESHOLD = 0.001  # ETH
NUM_MNEMONICS = 1000000
SLEEP_TIME = 0.01  # seconds between requests
ANKR_RPC_URL = "https://rpc.ankr.com/eth"

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
        return 0

# Main loop
start_time = time.time()

for i in range(NUM_MNEMONICS):
    # Show fixed progress every 100 mnemonics
    if i % 100 == 0:
        print(f"\nGenerated {i} of {NUM_MNEMONICS} mnemonics...")

    # Generate a 12-word mnemonic
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)

    # Derive seed and Ethereum address
    seed = Bip39SeedGenerator(mnemonic).Generate()
    bip44_ctx = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    account = bip44_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    address = account.PublicKey().ToAddress()

    # Check ETH balance
    balance = get_eth_balance(address)
    elapsed_time = time.time() - start_time
    speed = (i + 1) / elapsed_time

    # Dynamic console output
    sys.stdout.write(f"\r[{i + 1}/{NUM_MNEMONICS}] Checking address {address[:12]}... Speed: {speed:.2f} req/sec")
    sys.stdout.flush()

    time.sleep(SLEEP_TIME)

    if balance >= TARGET_BALANCE_THRESHOLD:
        print("\n\n=== Match Found ===")
        print(f"Mnemonic: {mnemonic}")
        print(f"Address: {address}")
        print(f"Balance: {balance:.6f} ETH")
        break

print("\n\nFinished scanning.")
