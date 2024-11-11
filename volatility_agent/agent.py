import asyncio
import os
import numpy as np
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.full_node_client import FullNodeClient
from dotenv import find_dotenv, load_dotenv
from giza.agents.model import GizaModel
from starknet_py.contract import Contract






async def main(client):
    # X is the data input you need to define
    file_path = "data/data_array.npy"

    X = np.load(file_path)
    print(X)

    # we create an instance of our Account
    account = Account(
            address=address,
            client=client,
            key_pair=KeyPair.from_private_key(private_key),
            chain=StarknetChainId.SEPOLIA,
        )

    # we create an instance of our Agent given the id
    model = GizaModel(
            id=930,
            version=1,
        )
        
    (result, request_id) = model.predict(
        input_feed={"input" :X}, verifiable=True, dry_run=True
    )


    contract = Contract.from_address(provider=account, address=address)

    sender = "321"
    recipient = "123"

    # Using only positional arguments
    nvocation = await contract.functions["transferFrom"].invoke_v1(
        sender=sender, recipient=recipient, amount=10000, max_fee=int(1e16)
    )

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    # First, make sure to generate private key and salt
    address = "0x025e0b4016442e75a1b5809c43d441920cde24c7b7b43a9015b4d83bb61c8796"
    private_key = os.environ.get("CLASS_HASH")
    class_hash = os.environ.get("CLASS_HASH")
    salt = 1234567890

    node_url = "https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_7/YqZibhgmuU767042gRepTUGKB5v99iUG"
    client = FullNodeClient(node_url=node_url)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(main(client))
