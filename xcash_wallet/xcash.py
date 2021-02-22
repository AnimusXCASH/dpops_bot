from xcash_wallet.xcashRpcWallet import WalletRpc

rpc_data = {
    "headers_daemon": {'content-type': 'application/json'},
    "json_rpc_url_wallet": "http://localhost:18285/json_rpc",
    "headers": {'Content-Type': 'application/json'}
}


class XcashManager:
    def __init__(self):
        self.xcash_rpc = WalletRpc(rpc_data=rpc_data)
