from xcash_dpops_api.delegateApi import DelegateApiAccess
from xcash_dpops_api.foundation import DpopsDelegates
from xcash_dpops_api.xcashExplorer import XcashExplorer
from xcash_dpops_api.dpopsCalculators import DpopsCalculator


class Dpops:
    """
    Wrapper for various APIs related to delegates and xcash
    """

    def __init__(self, dpops_api, delegate_name: str):
        self.foundation = "http://delegates.xcash.foundation/"
        self.delegate_api = DelegateApiAccess(dpops_api=dpops_api)
        self.delegates = DpopsDelegates()
        self.xcash_explorer = XcashExplorer()
        self.calculator = DpopsCalculator(delegate_name=delegate_name)
