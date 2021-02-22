import discord
from discord.ext import commands
from discord import Intents
from utils.tools import Helpers

cogs_to_load = ["cogs.help", 'cogs.autoFunctions', 'cogs.delegateQueries','cogs.botSetup',
                "delegate.delegateCommands", "delegate.voterCommands"]


class DiscordBot(commands.Bot):
    def __init__(self, dpops_wrapper, xcash_manager, backend_manager):
        helper = Helpers()
        self.bot_settings = helper.read_json_file(file_name='botSetup.json')
        super().__init__(
            command_prefix=commands.when_mentioned_or(self.bot_settings['command']),
            intents=Intents.all())
        self.remove_command('help')
        self.dpops_queries = dpops_wrapper
        self.voters_manager = backend_manager.voters
        self.bot_settings_manager = backend_manager.bot_settings_manager
        self.rpc_wallet = xcash_manager
        self.load_cogs()

    def load_cogs(self):
        notification_str = '+++++++++++++++++++++++++++++++++++++++ \n' \
                           'LOADING \COGS....        \n'
        for c in cogs_to_load:
            try:
                self.load_extension(c)
                notification_str += f'| {c} :smile: \n'
            except Exception as error:
                notification_str += f'| {c} --> {error}\n'
                raise
        notification_str += '+++++++++++++++++++++++++++++++++++++++'
        print(notification_str)

    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game('Monitoring Delegates'))
        print('DISCORD BOT : Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print('================================')

    def run(self):
        super().run(self.bot_settings['token'], reconnect=True)

    def get_command_str(self):
        return self.bot_settings['command']
