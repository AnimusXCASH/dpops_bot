from xcash_dpops_api.dpops import Dpops
from AutoTasks import AutomaticTasks, start_tasks
from DiscordBot import DiscordBot
from xcash_wallet.xcash import XcashManager
from backendManager.backend import BackendManager

if __name__ == "__main__":
    backend_manager = BackendManager()
    print("Checking required collections")
    backend_manager.integrity_check.check_collections()
    dpops_wrapper = Dpops()
    xcash_manager = XcashManager()
    bot = DiscordBot(dpops_wrapper, xcash_manager, backend_manager)
    auto_tasks = AutomaticTasks(dpops_wrapper, bot)
    task_starter = start_tasks(automatic_tasks=auto_tasks)
    bot.run()
    print("Done")
