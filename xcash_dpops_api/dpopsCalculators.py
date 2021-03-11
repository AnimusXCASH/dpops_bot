import requests


class DpopsCalculator:
    def __init__(self, delegate_name: str):
        self.delegate_name = delegate_name
        self.api = "http://calculator.x-node.es/api/v1/delegates"
        self.calculator_api = self.api + '/' + self.delegate_name

    def __process_request(self,api_link=None):
        if api_link:
            api = self.calculator_api + api_link
        else:
            api = self.calculator_api
        response = requests.get(api)
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
