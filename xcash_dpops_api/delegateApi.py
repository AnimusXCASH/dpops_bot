import requests


class DelegateApiAccess:
    def __init__(self, dpops_api):
        self.api = dpops_api
        self.statistics = '/shareddelegateswebsitegetstatistics'
        self.blocks_found = '/getblocksfound'
        self.public_address_info = '/getpublicaddressinformation'
        self.public_address_payment_info = '/getpublicaddresspaymentinformation'
        self.get_voters_list = '/getdelegatesvoterslist'

    @staticmethod
    def __process_request(api_link: str):
        response = requests.get(api_link)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}

    def get_stats(self):
        """
        Get delegate statistics
        """
        delegate_api = self.api + self.statistics
        return self.__process_request(api_link=delegate_api)

    def get_blocks_found(self):
        """
        Get all blocks found
        """
        delegate_api = self.api + self.blocks_found
        return self.__process_request(api_link=delegate_api)

    def get_last_block_found(self):
        """
        Get last found block
        """
        delegate_api = self.api + self.blocks_found
        response = requests.get(delegate_api)
        try:
            if response.status_code == 200:
                blocks = response.json()
                new_block_list = blocks[-1:]
                return new_block_list
            else:
                return {"error": f"Could not get response from server"}
        except Exception as e:
            return {"error": "There has been an exception. Please check get_last_block_found"}

    def pub_addr_info(self, pub_addr):
        """
        Get public address information
        """
        delegate_api = self.api + self.public_address_info + f"?public_address={pub_addr}"
        return self.__process_request(api_link=delegate_api)

    def public_address_payments(self, public_address: str):
        """
        Get all payments for public address from delegate
        """
        delegate_api = self.api + self.public_address_payment_info + f"?public_address={public_address}"
        return self.__process_request(api_link=delegate_api)
