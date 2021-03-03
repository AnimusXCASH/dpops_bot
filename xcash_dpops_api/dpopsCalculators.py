#     # http://calculator.x-node.es/api/v1/delegates/twinkie -> get the roi for the delegate twinkie with the default values (2M xcash for 30 days)
#     # http://calculator.x-node.es/api/v1/delegates/twinkie/20M -> get the roi for the delegate twinkie voting 20M with the default period (30 days)
#     # http://calculator.x-node.es/api/v1/delegates/twinkie/20M/10 -> get the roi for the delegate twinkie voting 20M xcash during 10 days
#

import requests


class DpopsCalculator:
    def __init__(self, delegate_name: str):
        self.delegate_name = delegate_name
        self.api = "http://calculator.x-node.es/api/v1/delegates/"
        self.calculator_api = self.api + '/' + self.delegate_name

    def __process_request(self, api_link: str = None):
        api_link = self.calculator_api + api_link
        response = requests.get(api_link)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}

    def thirty_day_roi(self):
        """
        30 day roi based on 2 mil stake
        """
        return self.__process_request()

    def thirty_day_roi_custom(self, amount: int):
        """
        30 day return based on the amount
        """
        custom_api = f'/{amount}M'
        return self.__process_request(api_link=custom_api)

    def custom_day_custom_amount_roi(self, amount: int, days: int):
        """
        30 day return based on the amount
        """
        custom_api = f'/{amount}M/{days}'
        return self.__process_request(api_link=custom_api)
