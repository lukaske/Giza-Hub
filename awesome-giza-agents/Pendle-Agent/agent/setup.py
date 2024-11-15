import os
from logging import getLogger

from addresses import ADDRESSES
from ape import Contract, accounts, networks
from dotenv import find_dotenv, load_dotenv

# logging.basicConfig(level=logging.INFO)

load_dotenv(find_dotenv())

dev_passphrase = "jabuk123"  ## Make sure to edit your .env file with your passphrase
network = "ethereum:mainnet-fork:foundry"  ## We ask the Ape Framework to locate our forked mainnet

if __name__ == "__main__":

    logger = getLogger("setup_logger")
    logger.propagate = False

    logger.warning("Initiationg setup process")

    networks.parse_network_choice(network).__enter__()

    eETH = Contract(ADDRESSES["eETH"])
    weETH = Contract(ADDRESSES["weETH"])
    eETH_decimals = eETH.decimals()
    weETH_decimals = weETH.decimals()
    eETH_LP = Contract(ADDRESSES["eETH_LP"])

    dev = accounts.load("505sol")  ## Change this to your account name
    dev.set_autosign(True, passphrase=dev_passphrase)
    dev.balance += 20 * int(1e18)  # Add 20 ETH to the account

    eETH_mint_amount = 8 * (10**eETH_decimals)  ## Mint 8 eETH

    with accounts.use_sender("505sol"):
        logger.warning(
            f"Staking Ether to get  {eETH_mint_amount/10**eETH_decimals} eETH"
        )
        eETH_LP.deposit(
            value=eETH_mint_amount, max_fee=10**10
        )  ## Deposit 8 ETH to get eETH
        logger.warning("Approving eETH to wrap to weETH")
        eETH.approve(
            weETH.address, eETH_mint_amount, max_fee=10**10
        )  ## Approve eETH to be wrapped to weETH
        weETH.wrap(eETH_mint_amount, max_fee=10**10)  ## Wrap eETH to weETH
        weETH_balance = weETH.balanceOf(dev)

    logger.warning(
        f"Dev Wallet has a balance of {weETH_balance/10**weETH_decimals} weETH"
    )
    logger.warning("Setup complete")
