"""

Executing calls to RPC XCASH Daemon

"""

import json
import requests


class XcashDaemon:

    def __init__(self, rpc_data):
        self.json_rpc_url = rpc_data['json_rpc_url_daemon']
        self.headers = rpc_data['headers_daemon']

    def get_block_height(self):
        try:

            rpc_input = {

                'method': "get_block_count"

            }

            rpc_input.update({"jsonrpc": "2.0", "id": "0"})

            response = requests.post(self.json_rpc_url, data=json.dumps(rpc_input), headers=self.headers)

            json_data = response.json()

            block_height = json_data['result']['count']

            return block_height

        except Exception as e:

            return None
