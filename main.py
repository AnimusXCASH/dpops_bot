from xcash_dpops_api.dpops import Dpops
from AutoTasks import AutomaticTasks, start_tasks
from DiscordBot import DiscordBot
from xcash_wallet.xcash import XcashManager
from backendManager.backend import BackendManager
from utils.tools import Helpers

if __name__ == "__main__":
    helper = Helpers()
    bot_settings = helper.read_json_file(file_name='botSetup.json')
    backend_manager = BackendManager()
    print("Checking required collections")
    backend_manager.integrity_check.check_collections()
    dpops_wrapper = Dpops(dpops_api=bot_settings["dpopsApi"], delegate_name=bot_settings["delegateName"],delegate_addr = bot_settings["delegatePublicKey"])
    xcash_manager = XcashManager()
    bot = DiscordBot(dpops_wrapper, xcash_manager, backend_manager)
    auto_tasks = AutomaticTasks(dpops_wrapper, bot)
    task_starter = start_tasks(automatic_tasks=auto_tasks)
    bot.run()
    print("Done")
