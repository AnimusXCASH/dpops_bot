import requests


class DelegateApiAccess:
    def __init__(self, dpops_api=None):
        self.api = "http://xpayment.x-network.eu"
        self.statistics = '/shareddelegateswebsitegetstatistics'
        self.blocks_found = '/getblocksfound'
        self.public_address_info = '/getpublicaddressinformation'
        self.public_address_payment_info = '/getpublicaddresspaymentinformation'
        self.get_voters_list = '/getdelegatesvoterslist'

    def __process_request(self, api_link: str):
        api_link = self.api + api_link
        response = requests.get(api_link)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}

    def get_stats(self):
        """
        Get delegate statistics
        """
        return self.__process_request(api_link=self.statistics)

    def get_blocks_found(self):
        """
        Get all blocks found
        """
        return self.__process_request(api_link=self.blocks_found)

    def get_last_block_found(self):
        """
        Get last found block
        """
        return self.__process_request(api_link=self.blocks_found)

    def pub_addr_info(self, pub_addr):
        """
        Get public address information
        """
        endpoint = self.public_address_info + f"?public_address={pub_addr}"
        return self.__process_request(api_link=endpoint)

    def public_address_payments(self, public_address: str):
        """
        Get all payments for public address from delegate
        """
        endpoint = self.public_address_payment_info + f"?public_address={public_address}"
        return self.__process_request(api_link=endpoint)
