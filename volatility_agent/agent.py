import asyncio
import os
import numpy as np
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.full_node_client import FullNodeClient
from dotenv import find_dotenv, load_dotenv
from giza.agents.model import GizaModel
from giza.agents import GizaAgent
from starknet_py.contract import Contract
from erc20 import approve_token, check_allowance


async def close_position(account, contract_address, close_params):
    # Connect to the contract
    contract = await Contract.from_address(address=contract_address, provider=account)

    try:
        # For Cairo 0 contracts, use invoke_v1
        call = await contract.functions["withdraw"].invoke_v1(
            **close_params, auto_estimate=True
        )

        # Wait for transaction
        # await account.client.wait_for_tx(call.transaction_hash)
        res = await call.wait_for_acceptance()
        print(res.hash)

        return call
    except Exception as e:
        # If v1 fails, try v3 (for Cairo 1+ contracts)
        try:
            call = await contract.functions["withdraw"].invoke_v3(
                **close_params, auto_estimate=True
            )

            # Wait for transaction
            # await account.client.wait_for_tx(call.transaction_hash)

            await call.wait_for_acceptance()

            return call
        except Exception as nested_e:
            print(f"v1 error: {e}")
            print(f"v3 error: {nested_e}")
            raise

async def execute_withdrawal(account, contract_address):
    withdrawal_params = {
        "id": int("0x140", 16),
        "pool_key": {
            "token0": int(
                "04718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d", 16
            ),
            "token1": int(
                "049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7", 16
            ),
            "fee": int("0x20c49ba5e353f80000000000000000", 16),
            "tick_spacing": int("0x3e8", 16),
            "extension": 0,
        },
        "bounds": {
            "lower": {"mag": int("0x6d600", 16), "sign": True},
            "upper": {"mag": int("0xfa00", 16), "sign": False},
        },
        "liquidity": int("0x21963d8949e0ca7c", 16),
        "min_token0": 0,
        "min_token1": 0,
        "collect_fees": True,
    }

    # Call mint function
    try:
        # Call mint function
        transaction = await close_position(account, contract_address, withdrawal_params)
        print(f"Transaction hash: {hex(transaction.hash)}")

        # # Wait for transaction receipt
        # receipt = await account.client.wait_for_tx(transaction.hash)
        # print(f"Transaction status: {receipt.status}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

        async def execute_mint_position(account, contract_address):
    mint_params = {
        "pool_key": {
            "token0": int(
                "04718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d", 16
            ),
            "token1": int(
                "049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7", 16
            ),
            "fee": int("0x20c49ba5e353f80000000000000000", 16),
            "tick_spacing": int("0x3e8", 16),
            "extension": 0,
        },
        "bounds": {
            "lower": {"mag": int("0x77a10", 16), "sign": True},
            "upper": {"mag": int("0x58610", 16), "sign": True},
        },
        "min_liquidity": int("0x35a818a2ecc5be4b", 16),
    }

    # Call mint function
    try:
        # Call mint function
        transaction = await mint_position(account, contract_address, mint_params)
        print(f"Transaction hash: {hex(transaction.transaction_hash)}")

        # Wait for transaction receipt
        receipt = await account.client.wait_for_tx(transaction.transaction_hash)
        print(f"Transaction status: {receipt.status}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

        # Helper function to determine whether to open or close a position based on volatility
async def check_volatility_and_act(account, contract_address, model, X):
    try:
        # Get the prediction result
        (result, request_id) = model.predict(
            input_feed={"input": X}, verifiable=True, dry_run=True
        )
        
        # Assuming the model outputs volatility in result['volatility']
        volatility = result.get('volatility', None)
        print(f"Predicted volatility: {volatility}")

        if volatility is None:
            raise ValueError("Model did not return a valid volatility value.")

        # Thresholds for opening/closing positions
        low_volatility_threshold = 0.2
        high_volatility_threshold = 0.5

        if volatility < low_volatility_threshold:
            print("Volatility is low. Proceeding to open a position.")
            await execute_mint_position(account, contract_address)
        elif volatility > high_volatility_threshold:
            print("Volatility is high. Proceeding to close the position.")
            await execute_withdrawal(account, contract_address)
        else:
            print("Volatility is within normal range. No action taken.")

    except Exception as e:
        print(f"Error during volatility check and action: {str(e)}")

async def mint_position(account, contract_address, mint_params):
    # Connect to the contract
    contract = await Contract.from_address(address=contract_address, provider=account)

    try:
        # Approve token0
        await approve_token(
            account,
            int(mint_params["pool_key"]["token0"]),
            int(contract_address.replace("0x", ""), 16),
        )

        # Approve token1
        await approve_token(
            account,
            int(mint_params["pool_key"]["token1"]),
            int(contract_address.replace("0x", ""), 16),
        )

        # Verify allowances
        allowance0 = await check_allowance(
            account,
            int(mint_params["pool_key"]["token0"]),
            account.address,
            int(contract_address.replace("0x", ""), 16),
        )
        allowance1 = await check_allowance(
            account,
            int(mint_params["pool_key"]["token1"]),
            account.address,
            int(contract_address.replace("0x", ""), 16),
        )

        print(f"Token0 allowance: {allowance0}")
        print(f"Token1 allowance: {allowance1}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

    try:
        # For Cairo 0 contracts, use invoke_v1
        call = await contract.functions["mint_and_deposit"].invoke_v1(
            **mint_params, auto_estimate=True
        )

        # Wait for transaction
        # await account.client.wait_for_tx(call.transaction_hash)
        res = await call.wait_for_acceptance()
        print(res.hash)

        return call
    except Exception as e:
        print(f"v1 error: {e}")
        raise


async def main(client):
    # Load the data for the model input
    file_path = "data/data_array.npy"
    X = np.load(file_path)
    print("Input data:", X)

    # Create an account instance
    account = Account(
        address=address,
        client=client,
        key_pair=KeyPair.from_private_key(private_key),
        chain=StarknetChainId.SEPOLIA,
    )

    # Create a Giza model instance
    model = GizaModel(
        id=930,
        version=1
    )

    # Define the contract address
    contract_address = "0x06a2aee84bb0ed5dded4384ddd0e40e9c1372b818668375ab8e3ec08807417e5"

    # Check the volatility and act accordingly
    await check_volatility_and_act(account, contract_address, model, X)

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    address = "0x025e0b4016442e75a1b5809c43d441920cde24c7b7b43a9015b4d83bb61c8796"
    private_key = os.environ.get("PRIVATE_KEY")
    node_url = "https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_7/YqZibhgmuU767042gRepTUGKB5v99iUG"
    client = FullNodeClient(node_url=node_url)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(client))
