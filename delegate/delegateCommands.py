from cogs.utils import customMessages
from discord.ext import commands
from delegate.tools.customMessages import embed_builder, delegate_stats, get_last_blocks
from discord import Colour
from datetime import datetime
from pprint import pprint


class XPaymentDelegateCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()
        self.xDelegate = self.bot.dpops_queries.xpayment

    @commands.group(aliases=["x"])
    async def delegate(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':joystick: __Available delegate stats__ :joystick: '
            description = "All commands dedicated to query delegate characteristics"
            list_of_values = [{"name": "Overall Statistics",
                               "value": f"```{self.command_string}delegate stats```\n"
                                        f"`Aliases: s`"},
                              {"name": "Review 5 last blocks",
                               "value": f"```{self.command_string}delegate blocks```\n"
                                        f"`Aliases: b`"}

                              ]
            await embed_builder(ctx=ctx, title=title, description=description, data=list_of_values,
                                destination=1, c=Colour.dark_orange())

    @delegate.command(aliases=["s"])
    async def stats(self, ctx):
        data = self.xDelegate.get_stats()
        if not data.get("error"):
            await delegate_stats(destination=ctx.author, data=data, thumbnail=self.bot.user.avatar_url)
        else:
            await ctx.author.send(content="It seems like there has been an API error. Please try again later")

    @delegate.command(aliases=["b"])
    async def blocks(self, ctx):
        data = self.xDelegate.get_blocks_found()
        await get_last_blocks(destination=ctx.author, blocks=data, thumbnail=self.bot.user.avatar_url)


def setup(bot):
    bot.add_cog(XPaymentDelegateCommands(bot))
