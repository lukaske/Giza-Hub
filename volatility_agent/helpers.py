from starknet_py.contract import Contract
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

import os
from erc20 import approve_token, check_allowance


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


async def main():
    # Setup node client (replace URL with your node URL)
    node_url = "https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_7/YqZibhgmuU767042gRepTUGKB5v99iUG"  # e.g., "https://your-rpc-node" or use a node provider
    client = FullNodeClient(node_url)

    # Setup account
    private_key = os.environ.get("PRIVATE_KEY2")
    account_address = (
        "0x00f6DA494c24996247E3E4B2E56b2fa2736B3b15735518a71636b29829c55229"
    )

    # Create account client
    key_pair = KeyPair.from_private_key(private_key)
    account = Account(
        client=client,
        address=account_address,
        key_pair=key_pair,
        chain=StarknetChainId.SEPOLIA,
    )

    # Contract address
    contract_address = (
        "0x06a2aee84bb0ed5dded4384ddd0e40e9c1372b818668375ab8e3ec08807417e5"
    )

    # # Execute mint position
    await execute_mint_position(account, contract_address)

    # Execute withdrawal
    # await execute_withdrawal(account, contract_address)


# Run the async function
import asyncio

asyncio.run(main())



# https://app.ekubo.org/positions/new?baseCurrency=ETH&quoteCurrency=STRK&tickLower=-64000&tickUpper=448000&initialTick=8797496
# https://app.ekubo.org/positions/new?baseCurrency=STRK&quoteCurrency=ETH&tickLower=-448000&tickUpper=64000
