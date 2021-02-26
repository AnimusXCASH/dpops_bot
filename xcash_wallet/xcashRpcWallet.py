import json
import requests


class WalletRpc:
    def __init__(self, rpc_data: dict):
        self.json_rpc_url = rpc_data['json_rpc_url_wallet']
        self.headers = rpc_data['headers']

    def get_balance(self, account_index=None):
        rpc_input = {
            "method": "get_balance",
        }

        if account_index is not None:
            rpc_input.update({"params": {"account_index": account_index}})

        rpc_input.update({"jsonrpc": "2.0", "id": "0"})

        response = requests.post(self.json_rpc_url, data=json.dumps(

            rpc_input), headers=self.headers)

        return response.json()

    def get_outgoing_transfers(self, last_processed_height:int):
        rpc_input = {
            'method': "get_transfers",
            'params': {"out": True,
                       "filter_by_height":True,
                       "min_height":last_processed_height -1
                       }
        }

        rpc_input.update({"jsonrpc": "2.0", "id": "0"})

        response = requests.post(self.json_rpc_url, data=json.dumps(rpc_input), headers=self.headers)

        return response.json()

    def get_last_outgoing_transfers(self, last_processed_height):
        rpc_input = {
            'method': "get_transfers",
            'params': { "filter_by_height": True,
                        "out": True,
                        "min_height": last_processed_height - 1
                       }
        }

        rpc_input.update({"jsonrpc": "2.0", "id": "0"})

        response = requests.post(self.json_rpc_url, data=json.dumps(rpc_input), headers=self.headers)

        return response.json()

    def get_transfers_by_tx_id(self, tx_id:str):
        rpc_input = {
            'method': "get_transfer_by_txid",
            'params': {"txid": tx_id
                       }
        }
        rpc_input.update({"jsonrpc": "2.0", "id": "0"})
        response = requests.post(self.json_rpc_url, data=json.dumps(rpc_input), headers=self.headers)

        return response.json()


