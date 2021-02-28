from discord.ext import commands
from cogs.utils import customMessages
from discord import Colour, TextChannel
from cogs.utils.customChecks import is_owner, is_public


class PaymentsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()

    @commands.command()
    @commands.check(is_public)
    @commands.check(is_owner)
    async def payments(self, ctx):
        title = 'Payments'
        description = f"Commands to apply delegate for payment notifications to channel. Everytime delegate sends" \
                      f" batch of payments/rewards to voters, basic batch details will be sent out."
        list_of_commands = [
            {"name": ":one: Batch payment notifications ",
             "value": f"```{self.command_string}payments apply <channel>```"},
            {"name": ":two: Activate Notifications",
             "value": f"```{self.command_string}payments on```"},
            {"name": ":three: Deactivate Notifications",
             "value": f"```{self.command_string}payments off```"},
        ]
        await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                           list_of_commands=list_of_commands)

    @payments.command()
    async def apply(self, ctx, channel: TextChannel):
        if self.bot.setting.update_settings_by_dict(setting_name="payment_notifications",
                                                    value={"channel": int(channel.id)}):
            await customMessages.system_message(ctx=ctx, c=Colour.green(), title="Daily Stats Notifications",
                                                error_details=f"You have successfully applied channel {channel} "
                                                              f"to batch payment notifications.",
                                                destination=ctx.channel)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="System Error",
                                                error_details="It seems like there haas been a backend issue."
                                                              " Please try again later or open github ticket "
                                                              "and let us know.",
                                                destination=ctx.channel)

    @payments.command()
    async def off(self, ctx):
        if self.bot.setting.update_settings_by_dict(setting_name="payment_notifications",
                                                    value={"status": int(0)}):
            await customMessages.system_message(ctx=ctx, c=Colour.green(), title="Daily Stats Notifications",
                                                error_details=f"You have successfully turned Delegate Paymnet "
                                                              f"Notifications to channel OFF. To reactivate them use"
                                                              f" ***{self.command_string}payments on***, and "
                                                              f" to change the channel where notifications on batch "
                                                              f"payments are sent use {self.command_string}apply "
                                                              f"<#discordChannel>",
                                                destination=ctx.channel)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="System Error",
                                                error_details="It seems like there haas been a backend issue."
                                                              " Please try again later or open github ticket "
                                                              "and let us know.",
                                                destination=ctx.channel)

    @payments.command()
    async def on(self, ctx):
        if self.bot.setting.update_settings_by_dict(setting_name="payment_notifications",
                                                    value={"status": int(1)}):
            await customMessages.system_message(ctx=ctx, c=Colour.green(), title="Daily Stats Notifications",
                                                error_details=f"You have successfully turned Delegate Paymnet "
                                                              f"Notifications to channel ON. To deactivate them use"
                                                              f" ***{self.command_string}payments off***, and "
                                                              f" to change the channel where notifications on batch "
                                                              f"payments are sent, use {self.command_string}apply "
                                                              f"<#discordChannel>",
                                                destination=ctx.channel)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="System Error",
                                                error_details="It seems like there haas been a backend issue."
                                                              " Please try again later or open github ticket "
                                                              "and let us know.",
                                                destination=ctx.channel)


def setup(bot):
    bot.add_cog(PaymentsManager(bot))
