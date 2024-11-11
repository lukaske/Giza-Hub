from starknet_py.net.full_node_client import FullNodeClient



node_url = "https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_7/YqZibhgmuU767042gRepTUGKB5v99iUG"
client = FullNodeClient(node_url=node_url)
call_result = client.get_block_sync(block_number=1)
