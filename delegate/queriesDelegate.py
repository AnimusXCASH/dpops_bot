from discord.ext import commands
from delegate.tools.customMessages import delegate_stats, embed_builder
from discord import Colour


class DelegateQueries(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()

    @commands.group(aliases=['d'])
    async def delegate(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':judge: Delegate Informational Commands'
            description = f"Informational commands on the delegate"
            list_of_commands = [
                {"name": ":chart_with_upwards_trend: Stats on-demand",
                 "value": f"```{self.command_string}delegate stats```\n"
                          f"`Aliases: s`"}
            ]
            await embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                data=list_of_commands)

    @delegate.command(aliases=["s"])
    async def stats(self, ctx):
        stats = self.bot.dpops_queries.delegate_api.get_stats()

        await delegate_stats(destination=ctx.author, data=stats, thumbnail=self.bot.user.avatar_url)


def setup(bot):
    bot.add_cog(DelegateQueries(bot))
