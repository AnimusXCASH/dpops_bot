from xcash_dpops_api.delegateApi import DelegateApiAccess


class Dpops:
    def __init__(self,dpops_api):
        self.delegate_api = DelegateApiAccess(dpops_api=dpops_api)
