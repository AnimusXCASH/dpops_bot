from pymongo import MongoClient
from backendManager.integrityCheck import IntegrityCheck
from backendManager.votersManager import VotersManager
from backendManager.botSettingsManager import BotSettingsManager


class BackendManager:
    def __init__(self):
        self.connection = MongoClient("mongodb://127.0.0.1:27017", maxPoolSize=20)
        self.integrity_check = IntegrityCheck(connection=self.connection)
        self.voters = VotersManager(connection=self.connection)
        self.bot_settings_manager = BotSettingsManager(connection=self.connection)
