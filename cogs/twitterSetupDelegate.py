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

    async def stats_notifications_manager(self, ctx, setting_name: str, status_code: int, funct: str, selection):
        if self.bot.setting.update_settings_by_dict(setting_name=setting_name,
                                                    value={"status": int(status_code)}):
            await customMessages.system_message(ctx=ctx, c=Colour.green(), title=f"{funct} Twitter Notifications",
                                                error_details=f"You have successfully set/updated settings to "
                                                              f"***{selection.upper()}***",
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
                 "value": f"```{self.command_string}twitter rates <on/off>```"},
                {"name": "Dpops Delegate Vote Initiative",
                 "value": f"```{self.command_string}twitter vote <on/off>```"},
                {"name": ":warning: Warning ",
                 "value": f"Be sure that the bot has required permissions to view and write to the channel, "
                          f"where stats will be sent. "}

            ]
            await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                               list_of_commands=list_of_commands)

    @twitter.command()
    async def daily(self, ctx, on_off: str):
        status = on_off.lower()
        if status and status in ["on", "off"]:
            status_code = self.get_status_number(status=status)
            await self.stats_notifications_manager(ctx=ctx, setting_name="t_del_daily",
                                                   status_code=status_code, funct='Daily Delegate', selection=on_off)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Wrong Status",
                                                error_details=f"You have provided wrong status. Available are"
                                                              f" ***on/off*** while yours was {status}",
                                                destination=ctx.channel)

    @twitter.command()
    async def block(self, ctx, on_off: str):
        status = on_off.lower()
        if status and status in ["on", "off"]:
            status_code = self.get_status_number(status=status)
            await self.stats_notifications_manager(ctx=ctx, setting_name="t_new_block",
                                                   status_code=status_code, funct='New Block', selection=on_off)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Wrong Status",
                                                error_details=f"You have provided wrong status. Available are"
                                                              f" ***on/off*** while yours was {status}",
                                                destination=ctx.channel)

    @twitter.command()
    async def rates(self, ctx, on_off: str):
        status = on_off.lower()
        if status and status in ["on", "off"]:
            status_code = self.get_status_number(status=status)
            await self.stats_notifications_manager(ctx=ctx, setting_name="t_return_rate",
                                                   status_code=status_code, funct="ROI", selection=on_off)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Wrong Status",
                                                error_details=f"You have provided wrong status. Available are"
                                                              f" ***on/off*** while yours was {status}",
                                                destination=ctx.channel)

    @twitter.command()
    async def vote(self, ctx, on_off):
        status = on_off.lower()
        if status and status in ["on", "off"]:
            status_code = self.get_status_number(status=status)
            await self.stats_notifications_manager(ctx=ctx, setting_name="t_call_to_vote",
                                                   status_code=status_code, funct='Call to vote', selection=on_off)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Wrong Status",
                                                error_details=f"You have provided wrong status. Available are"
                                                              f" ***on/off*** while yours was {status}",
                                                destination=ctx.channel)

    @twitter.command()
    async def payments(self, ctx, on_off):
        status = on_off.lower()
        if status and status in ["on", "off"]:
            status_code = self.get_status_number(status=status)
            await self.stats_notifications_manager(ctx=ctx, setting_name="t_payment_batch",
                                                   status_code=status_code, funct='Batch Payments', selection=on_off)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Wrong Status",
                                                error_details=f"You have provided wrong status. Available are"
                                                              f" ***on/off*** while yours was {status}",
                                                destination=ctx.channel)


def setup(bot):
    bot.add_cog(TwitterSetupCommands(bot))
