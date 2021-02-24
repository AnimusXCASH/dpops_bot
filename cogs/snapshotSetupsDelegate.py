from discord.ext import commands
from cogs.utils import customMessages
from discord import Colour, TextChannel
from cogs.utils.customChecks import is_owner, is_public


class DelegateSnapshotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()

    @staticmethod
    def get_status_number(status: str):
        if status == 'on':
            return 1
        elif status == 'off':
            return 0

    @commands.group()
    @commands.check(is_public)
    @commands.check(is_owner)
    async def stats(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':sos: __System Commands :sos: '
            description = f"Available commands to operate with automatic statistical notifications. "
            list_of_commands = [
                {"name": "Daily Stats Notifications",
                 "value": f"```{self.command_string}stats daily <#TextChannel> <on/off>```"},
                {"name": "Hourly Stats Notifications",
                 "value": f"```{self.command_string}stats hourly <#TextChannel> <on/off>```"},
                {"name": ":warning: Warning ",
                 "value": f"Be sure that the bot has required permissions to view and write to the channel, "
                          f"where stats will be sent. "}

            ]
            await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                               list_of_commands=list_of_commands)

    @stats.command()
    async def daily(self, ctx, chn: TextChannel, status: str):
        """
        Operate with daily settings on notifications
        """
        status = status.lower()
        if status and status in ["on", "off"]:
            status_code = self.get_status_number(status=status)

            if self.bot.setting.update_settings_by_dict(setting_name="delegate_daily",
                                                        value={"status": int(status_code),
                                                               "channel": int(chn.id)}):
                await customMessages.system_message(ctx=ctx, c=Colour.green(), title="Daily Stats Notifications",
                                                    error_details=f"You have successfully set/updated ***Daily "
                                                                  f"statistic monitor*** for delegate @ 23:59:59 every"
                                                                  f" day on ***{chn}*** to ***{status.upper()}***",
                                                    destination=ctx.channel)
            else:
                await customMessages.system_message(ctx=ctx, c=Colour.red(), title="System Error",
                                                    error_details="It seems like there haas been a backend issue."
                                                                  " Please try again later or open github ticket "
                                                                  "and let us know.",
                                                    destination=ctx.channel)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Wrong Status",
                                                error_details=f"You have provided wrong status. Available are"
                                                              f" ***on/off*** while yours was {status}",
                                                destination=ctx.channel)

    @stats.command()
    async def hourly(self, ctx, chn: TextChannel, status: str):
        """
        Operate with hourly operations
        """
        status = status.lower()
        if status and status in ["on", "off"]:
            status_code = self.get_status_number(status=status)
            if self.bot.setting.update_settings_by_dict(setting_name="delegate_hourly",
                                                        value={"status": int(status_code),
                                                               "channel": int(chn.id)}):
                await customMessages.system_message(ctx=ctx, c=Colour.green(), title="Hourly Stats Notifications",
                                                    error_details=f"You have successfully set/updated ***Hourly "
                                                                  f"statistic monitor*** every hour on channel"
                                                                  f" ***{chn}*** to ***{status.upper()}***",
                                                    destination=ctx.channel)
            else:
                await customMessages.system_message(ctx=ctx, c=Colour.red(), title="System Error",
                                                    error_details="It seems like there haas been a backend issue."
                                                                  " Please try again later or open github ticket "
                                                                  "and let us know.",
                                                    destination=ctx.channel)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Wrong Status",
                                                error_details=f"You have provided wrong status. Available are"
                                                              f" ***on/off*** while yours was {status}",
                                                destination=ctx.channel)

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Missing required permission",
                                                error_details="In order to be able to access this area of "
                                                              " commands, you MUST be a Discord Server Owner and "
                                                              "command executed on public channel of the community "
                                                              "where bot has access to, so ownership rights can be "
                                                              "checked.")

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Channel Not Found",
                                                error_details=f"Provided channel could not be found on your server. "
                                                              f"Please tag the channel #ChannelName. ")

    @hourly.error
    async def hourly_error(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Channel Not Found",
                                                error_details=f"Provided channel could not be found on your server. "
                                                              f"Please tag the channel #ChannelName. ",
                                                destination=ctx.channel)


def setup(bot):
    bot.add_cog(DelegateSnapshotCommands(bot))
