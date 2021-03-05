from discord.ext import commands
from cogs.utils import customMessages
from discord import Colour


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()

    @commands.group()
    async def help(self, ctx):
        title = ':sos: ___Available Command Categories__ :sos: '
        description = f"Available sub commands for `{self.command_string}help`"
        list_of_commands = [
            {"name": ":judge: Delegate on-demand",
             "value": f"```{self.command_string}delegate```\n"
                      f"`Alias:d`"},
            {"name": ":ballot_box: Commands for voter",
             "value": f"```{self.command_string}voter```"},
            {"name": ":toolbox: Commands for server owner",
             "value": f"```{self.command_string}sys```"},
            {"name": ":toolbox: Commands to query DPOPS network",
             "value": f"```{self.command_string}dpops```"},

        ]
        await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                           list_of_commands=list_of_commands)


def setup(bot):
    bot.add_cog(HelpCommands(bot))
