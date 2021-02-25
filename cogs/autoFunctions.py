from discord import Embed, Colour
from discord.ext import commands
from cogs.utils import customMessages


class AutoFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        """
        Global error for on command error
        """
        try:
            await ctx.message.delete()
        except Exception:
            pass

        if isinstance(exception, commands.CommandNotFound):
            title = '__Command Error__'
            message = f'Command `{ctx.message.content}` is not implemented/active yet or it does not exist! Please' \
                      f'type `{self.command_string}help` to check available commands.'
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title=title, error_details=message)

        elif isinstance(exception, commands.MissingRequiredArgument):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title=f'Missing required argument',
                                                error_details=f'{exception}')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            await ctx.message.delete()
        except Exception:
            pass


def setup(bot):
    bot.add_cog(AutoFunctions(bot))
