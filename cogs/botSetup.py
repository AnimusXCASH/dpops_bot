from discord.ext import commands
from cogs.utils import customMessages
from discord import Colour, TextChannel
from cogs.utils.customChecks import is_owner, is_public


class BotSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()

    @commands.command()
    @commands.check(is_public)
    @commands.check(is_owner)
    async def owner(self, ctx):
        title = ':sos: __System Commands :sos: '
        description = f"All available commands for owner of the server"
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

    @commands.group(aliases=["block"])
    @commands.check(is_public)
    @commands.check(is_owner)
    async def blocks(self, ctx):
        if ctx.invoked_subcommand is None:
            title = 'How to set-up delegate block monitor'
            description = f"Follow the instructions in order to setup block monitoring"
            list_of_commands = [
                {"name": ":one: Set channel",
                 "value": f"```{self.command_string}blocks chn <#discord.Channel>```"},
                {"name": ":two: Set Starting height",
                 "value": f"```{self.command_string}blocks height <block height INT>```"},
                {"name": ":three: Set Starting height",
                 "value": f"```{self.command_string}blocks monitor <on/off>```"},
                {"name": ":warning: Warning ",
                 "value": f"Be sure that the bot has required permissions to view and write to the channel, "
                          f"where stats will be sent. "}

            ]
            await customMessages.embed_builder(ctx=ctx, c=Colour.green(), title=title, description=description,
                                               list_of_commands=list_of_commands)

    @blocks.command()
    async def height(self, ctx, block_height: int):
        if self.bot.setting.update_settings_by_dict(setting_name="new_block",
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

    @blocks.command()
    async def chn(self, ctx, channel: TextChannel):
        if self.bot.setting.update_settings_by_dict(setting_name="new_block",
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

    @blocks.command()
    async def monitor(self, ctx, status_type: str):
        current = self.bot.setting.get_setting(setting_name='new_block')
        if current["channel"] > 0 and current["value"] > 0:
            if status_type.lower() in ['on', 'off']:
                if status_type.lower() == "on":
                    message = "You have successfully turned ***ON*** block monitor."
                    status_code = 1
                else:
                    message = "You have successfully turned ***OFF*** block monitor"
                    status_code = 0

                if self.bot.setting.update_settings_by_dict(setting_name="new_block",
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
        else:
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Set-up incomplete",
                                                error_details=f"You have not set both of the required properties. "
                                                              f"Channel and starting block height need to be provided"
                                                              f" first before you can activate block monitor.\n"
                                                              f" Current Status:"
                                                              f"> Block Height: {current['value']}\n"
                                                              f"> Channel: {current['channel']}",
                                                destination=ctx.channel)

    @owner.error
    async def owner_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Missing required permission",
                                                error_details="In order to be able to access this area of "
                                                              " commands, you MUST be a Discord Server Owner and "
                                                              "command executed on channel of the community where"
                                                              " bot has access to.",
                                                destination=ctx.channel)

    @blocks.error
    async def blocks_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await customMessages.system_message(ctx=ctx, c=Colour.red(), title="Missing required permission",
                                                error_details="In order to be able to access this area of "
                                                              " commands, you MUST be a Discord Server Owner and "
                                                              "command executed on channel of the community where"
                                                              " bot has access to.",
                                                destination=ctx.channel)


def setup(bot):
    bot.add_cog(BotSetup(bot))
