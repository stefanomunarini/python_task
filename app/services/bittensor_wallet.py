import os

import bittensor
from bittensor import Balance
# from bittensor.wallet import Wallet
from bittensor_wallet import Keypair, Wallet

# TODO REMOVE THIS FILE?

# Your faucet mnemonic
mnemonic = "diamond like interest affair safe clarify lawsuit innocent beef van grief color"

def get_faucet_wallet():
    keypair = Keypair.create_from_mnemonic(mnemonic)
    return Wallet(hotkey=keypair.ss58_address)

def transfer():

    faucet_wallet = get_faucet_wallet()
    destination = os.getenv("WALLET_HOTKEY")

    subtensor = bittensor.subtensor(network="finney")

    response = subtensor.transfer(
        wallet=faucet_wallet,
        dest=destination,
        amount=Balance(40.0),
    )

    print(f"Transfer success! Block: {response}")
