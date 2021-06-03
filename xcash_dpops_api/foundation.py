import requests


class DpopsDelegates:
    def __init__(self):
        self.api = "http://delegates.xcash.foundation/"
        self.delegates = 'getdelegates'
        self.get_delegate_stats = 'getdelegatesstatistics'
        self.get_delegate_info = 'getdelegatesinformation'
        self.get_delegates_voters = 'getdelegatesvoterslist'
        self.get_round_statistics = 'getroundstatistics'
        self.delegates_stats = "delegateswebsitegetstatistics"

    def __process_request(self, api_link: str):
        api_link = self.api + api_link
        response = requests.get(api_link)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Could not get response from server"}

    def get_global_dpops_stats(self):
        global_stats = self.api + self.delegates_stats
        return self.__process_request(api_link=global_stats)

    def get_delegates(self):
        return self.__process_request(api_link=self.delegates)

    def delegate_stats(self, delegate: str):
        delegate_api = self.get_delegate_stats + "?" + f'parameter1={delegate}'
        return self.__process_request(api_link=delegate_api)

    def delegate_info(self, delegate: str):
        delegate_api = self.get_delegate_stats + "?" + f'parameter1={delegate}'
        return self.__process_request(api_link=delegate_api)

    def get_delegate_voters(self, delegate):
        delegate_api = self.get_delegate_stats + "?" + f'parameter1={delegate}'
        return self.__process_request(api_link=delegate_api)
