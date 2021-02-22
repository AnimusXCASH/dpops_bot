import requests


class DelegateApiAccess:
    def __init__(self,dpops_api):
        self.api = dpops_api
        self.statistics = '/shareddelegateswebsitegetstatistics'
        self.blocks_found = '/getblocksfound'
        self.public_address_info = '/getpublicaddressinformation'
        self.public_address_payment_info = '/getpublicaddresspaymentinformation'
        self.get_voters_list = '/getdelegatesvoterslist'

    def get_stats(self):
        delegate_api = self.api + self.statistics
        response = requests.get(delegate_api)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}

    def get_blocks_found(self):
        delegate_api = self.api + self.blocks_found
        response = requests.get(delegate_api)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}

    def get_last_block_found(self):
        delegate_api = self.api + self.blocks_found
        response = requests.get(delegate_api)
        if response.status_code == 200:
            blocks = response.json()
            new_block_list = blocks[-1:]
            return new_block_list
        else:
            return {"error": f"Could not get response from server"}

    def pub_addr_info(self, pub_addr):
        delegate_api = self.api + self.public_address_info + f"?public_address={pub_addr}"
        response = requests.get(delegate_api)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}

    def public_address_payments(self, public_address: str):
        delegate_api = self.api + self.public_address_payment_info+f"?public_address={public_address}"
        response = requests.get(delegate_api)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}
