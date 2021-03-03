import requests


class XcashExplorer:
    def __init__(self):
        self.xcash_price = "https://min-api.cryptocompare.com/data/price?fsym=XCASH&tsyms=USD"

    @staticmethod
    def __process_request(api_link: str):
        response = requests.get(api_link)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}

    def price(self):
        """
        Returns error key or usd key if conversion
        """
        response = requests.get(self.xcash_price)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}
