from xcash_wallet.xcashDaemon import XcashDaemon
from xcash_wallet.xcashRpcWallet import WalletRpc

rpc_data = {
    "json_rpc_url_daemon": "http://xpayment.x-network.eu:18281/json_rpc",
    "headers_daemon": {'content-type': 'application/json'},
    "json_rpc_url_wallet": "http://localhost:18285/json_rpc",
    "headers": {'Content-Type': 'application/json'}
}


class XcashManager:
    def __init__(self):
        self.xcash_daemon = XcashDaemon(rpc_data=rpc_data)
        self.xcash_rpc = WalletRpc(rpc_data=rpc_data)
