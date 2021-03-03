from xcash_dpops_api.delegateApi import DelegateApiAccess
from xcash_dpops_api.foundation import DpopsDelegates
from xcash_dpops_api.xcashExplorer import XcashExplorer


class Dpops:
    """
    Wrapper for various APIs related to delegates and xcash
    """

    def __init__(self, dpops_api):
        self.foundation = "http://delegates.xcash.foundation/"
        self.delegate_api = DelegateApiAccess(dpops_api=dpops_api)
        self.delegates = DpopsDelegates(self.foundation)
        self.xcash_explorer = XcashExplorer()
