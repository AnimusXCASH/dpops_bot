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
        title = 'Payment Notifications'
        description = f"Commands to apply delegate for payment notifications to channel. Everytime delegate sends" \
                      f" batch of payments/rewards to voters, basic batch details will be sent out."
        list_of_commands = [
            {"name": "Apply for delegate stats notifications",
             "value": f"```{self.command_string}stats```"},
            {"name": "Apply for delegate block tracking",
             "value": f"```{self.command_string}blocks```"},
            {"name": "Delegate payment notifications",
             "value": f"```{self.command_string}payments```"}
        ]
        await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                           list_of_commands=list_of_commands)



def setup(bot):
    bot.add_cog(PaymentsManager(bot))

