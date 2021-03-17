from discord.ext import commands
from cogs.utils import customMessages
from discord import Colour, TextChannel
from cogs.utils.customChecks import is_owner, is_public


class TwitterSetupCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()

    @staticmethod
    def get_status_number(status: str):
        if status == 'on':
            return 1
        elif status == 'off':
            return 0

    async def stats_notifications_manager(self, ctx, setting_name: str, chn: TextChannel, status_code: int,
                                          status: str, frame: str):
        if self.bot.setting.update_settings_by_dict(setting_name=setting_name,
                                                    value={"status": int(status_code),
                                                           "channel": int(chn.id)}):
            await customMessages.system_message(ctx=ctx, c=Colour.green(), title=f"{frame} Stats Notifications",
                                                error_details=f"You have successfully set/updated ***{frame} "
                                                              f"statistic monitor*** on channel"
                                                              f" ***{chn}*** to ***{status.upper()}***",
                                                destination=ctx.channel)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="System Error",
                                                error_details="It seems like there haas been a backend issue."
                                                              " Please try again later or open github ticket "
                                                              "and let us know.",
                                                destination=ctx.channel)

    @commands.group(alias=["t", "bird", "tweet"])
    @commands.check(is_public)
    @commands.check(is_owner)
    async def twitter(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':bird:  __System Commands__ :bird:  '
            description = f"Setup twitter auto notifications"
            list_of_commands = [
                {"name": "Activate daily delegate stats",
                 "value": f"```{self.command_string}twitter daily <on/off>```"},
                {"name": "New block tweets",
                 "value": f"```{self.command_string}twitter block <on/off>```"},
                {"name": "Dpops return rate showcase",
                 "value": f"```{self.command_string}twitter reward <on/off>```"},
                {"name": "Dpops Delegate Vote Initiative",
                 "value": f"```{self.command_string}twitter vote <on/off>```"},
                {"name": ":warning: Warning ",
                 "value": f"Be sure that the bot has required permissions to view and write to the channel, "
                          f"where stats will be sent. "}

            ]
            await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                               list_of_commands=list_of_commands)


def setup(bot):
    bot.add_cog(TwitterSetupCommands(bot))
