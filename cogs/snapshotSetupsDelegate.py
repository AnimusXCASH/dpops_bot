from discord.ext import commands
from cogs.utils import customMessages
from discord import Colour, TextChannel
from cogs.utils.customChecks import is_owner, is_public


class DelegateSnaphostCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()

    @staticmethod
    def get_status_number(status: str):
        if status == 'on':
            return 1
        elif status == 'off':
            return 2

    @commands.group()
    @commands.check(is_public)
    @commands.check(is_owner)
    async def stats(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':sos: __System Commands :sos: '
            description = f"This section of commands is available only for the owner of the community"
            list_of_commands = [
                {"name": "Daily Stats Notifications",
                 "value": f"```{self.command_string}stats daily <#TextChannel> <on/off>```"},
                {"name": "Hourly Stats Notifications",
                 "value": f"```{self.command_string}stats hourly <#TextChannel> <on/off>```"}
            ]
            await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                               list_of_commands=list_of_commands)

    @stats.command
    async def daily(self, ctx, chn: TextChannel, status: str):
        status = status.lower()
        if status and status in ["on", "off"]:
            status_code = self.get_status_number(status=status)
            if self.bot.bot_settings_manager.update_settings_by_dict(setting_name="delegate_daily",
                                                                  value={"status": int(status_code),
                                                                         "channel": int(chn.id)}):
            else:
                print("fail the city")
        else:
            print('Wrong status chosen')

    @stats.command()
    async def hourly(self, ctx, chn: TextChannel, status: str):
        status = status.lower()
        if status and status in ["on", "off"]:
            status_code = self.get_status_number(status=status)
            if self.bot.bot_settings_manager.update_settings_by_dict(setting_name="delegate_hourly",
                                                                  value={"status": int(status_code),
                                                                         "channel": int(chn.id)}):
                print("Updated successfully")
            else:
                print("Faild the city")
        else:
            print('Wrong status chosen')

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Missing required permission",
                                                error_details="In order to be able to access this area of "
                                                              " commands, you MUST be a Discord Server Owner and "
                                                              "command executed on public channel of the community "
                                                              "where bot has access to.",
                                                destination=ctx.channel)


def setup(bot):
    bot.add_cog(DelegateSnaphostCommands(bot))
