class BotSettingsManager:
    def __init__(self, connection):
        self.connection = connection
        self.dpops_delegate = self.connection['DpopsDelegate']
        self.bot_settings = self.dpops_delegate.botSettings

    def get_setting(self, setting_name: str):
        data = self.bot_settings.find_one({"setting": setting_name},
                                          {"_id": 0})
        return data

    def get_all_settings(self):
        data = list(self.bot_settings.find({}))
        return data

    def update_settings_by_dict(self, setting_name: str, value: dict):
        try:
            result = self.bot_settings.update_one({"setting": setting_name},
                                                  {"$set": value})
            print(result)
            return result.modified_count > 0
        except Exception as e:
            return False
