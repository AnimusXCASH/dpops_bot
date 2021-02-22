from discord.ext import commands
from cogs.utils import customMessages
from discord import Colour, TextChannel, ChannelType


def is_owner(ctx):
    return int(ctx.message.author.id) == int(ctx.message.guild.owner.id)


def is_public(ctx):
    return ctx.message.channel.type != ChannelType.private


class BotSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()

    @commands.group()
    @commands.check(is_public)
    @commands.check(is_owner)
    async def sys(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':sos: __System Commands :sos: '
            description = f"This section of commands is available only for the owner of the community"
            list_of_commands = [
                {"name": "Bot Setup Categories",
                 "value": f"```{self.command_string}sys set```"}
            ]
            await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                               list_of_commands=list_of_commands)

    @sys.group()
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':sos: __Setup various auto notifications'
            description = f"This section of commands is available only for the owner of the community"
            list_of_commands = [
                {"name": "Operate with delegate Block Tracker settings",
                 "value": f"```{self.command_string}set block```"}
            ]
            await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                               list_of_commands=list_of_commands)

    @set.group()
    async def block(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':sos: __Available sub commands for setting Delegate block tracker'
            description = f"In order for delegate block tracker to functional optimally you need to " \
                          f"execute successfully all commands presented below. with :three: beeing the last one"
            list_of_commands = [
                {"name": ":one: Set starting block height",
                 "value": f"```{self.command_string}sys set block height <height>```"},
                {"name": ":two: Set channel for notifications",
                 "value": f"```{self.command_string}sys set block chn <#discord.Channel>```"},
                {"name": ":three: Turn On/Off block monitor",
                 "value": f"```{self.command_string}sys set block monitor <on/off>```"}
            ]
            await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                               list_of_commands=list_of_commands)

    @block.command()
    async def height(self, ctx, block_height: int):
        if self.bot.bot_settings_manager.update_settings_by_dict(setting_name="new_block",
                                                                 value={"value": int(block_height)}):
            await customMessages.system_message(ctx=ctx, c=Colour.green(), title="Block Height Setup",
                                                error_details=f"You have successfully set starting block height to "
                                                              f"***{block_height}***",
                                                destination=ctx.channel)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="System Error",
                                                error_details="It seems like there haas been a backend issue."
                                                              " Please try again later or open github ticket and let "
                                                              "us know.",
                                                destination=ctx.channel)

    @block.command()
    async def chn(self, ctx, channel: TextChannel):
        if self.bot.bot_settings_manager.update_settings_by_dict(setting_name="new_block",
                                                                 value={"channel": int(channel.id)}):
            await customMessages.system_message(ctx=ctx, c=Colour.green(), title="Block Channel Setup",
                                                error_details=f"You have successfully set channel ***{channel}*** "
                                                              f"(ID: {channel.id}) for notifications once your delegate "
                                                              f"produces new block.",
                                                destination=ctx.channel)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="System Error",
                                                error_details="It seems like there haas been a backend issue."
                                                              " Please try again later or open github ticket and let "
                                                              "us know.",
                                                destination=ctx.channel)

    @block.command()
    async def monitor(self, ctx, status_type: str):
        if status_type.lower() in ['on', 'off']:
            if status_type.lower() == "on":
                message = "You have successfully turned ***ON*** block monitor."
                status_code = 1
            else:
                message = "You have successfully turned ***OFF*** block monitor"
                status_code = 0

            if self.bot.bot_settings_manager.update_settings_by_dict(setting_name="new_block",
                                                                     value={"status": int(status_code)}):
                await customMessages.system_message(ctx=ctx, c=Colour.green(), title="Monitoring Status",
                                                    error_details=message,
                                                    destination=ctx.channel)
            else:
                await customMessages.system_message(ctx=ctx, c=Colour.red(), title="System Error",
                                                    error_details="It seems like there haas been a backend issue."
                                                                  " Please try again later or open github ticket and "
                                                                  "let us know.",
                                                    destination=ctx.channel)
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Wrong status provided",
                                                error_details=f"Allowed status types are either ***ON*** or ***OFF***. You "
                                                              f"have provided {status_type}",
                                                destination=ctx.channel)

    @chn.error
    async def chn_error(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Channel Not Found",
                                                error_details=f"Provided channel could not be found on your server. "
                                                              f"Please tag the channel #ChannelName. ",
                                                destination=ctx.channel)

    @height.error
    async def height_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Wrong Block Height form provided",
                                                error_details="Block height needs to be provided as INTEGER",
                                                destination=ctx.channel)

    @sys.error
    async def sys_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Missing required permission",
                                                error_details="In order to be able to access this area of "
                                                              " commands, you MUST be a Discord Server Owner and "
                                                              "command executed on channel of the community where"
                                                              " bot has access to.",
                                                destination=ctx.channel)


def setup(bot):
    bot.add_cog(BotSetup(bot))
