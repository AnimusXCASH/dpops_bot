from discord.ext import commands
from delegate.tools.customMessages import embed_builder, delegate_stats, get_last_blocks, get_last_payments, state_info, \
    sys_message
from discord import Colour, Embed
from re import match


class VoterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()
        self.xDelegate = self.bot.dpops_queries.xpayment

    @commands.group(aliases=["v"])
    async def voter(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':joystick: __Available delegate stats__ :joystick: '
            description = "All commands dedicated to all voters who have voted for x-payment world delegate." \
                          "you can use ***v*** as a synonym for ***voter***"
            list_of_values = [{"name": ":cowboy: Activate Profile",
                               "value": f"```{self.command_string}voter management```"
                                        f"`Aliases: mng`"},
                              {"name": ":mag_right: Check Last 4 payments",
                               "value": f"```{self.command_string}voter payments <public address>```\n"
                                        f"`Aliases: p`"},
                              {"name": ":mag_right: Check current state in Delegate",
                               "value": f"```{self.command_string}voter state <public address>```\n"
                                        f"`Aliases: nfo, i`"},
                              {"name": ":warning: Important :warning: ",
                               "value": f"`If you have registered yourself into Discord system than ***public address***"
                                        f" is not needed when executing commands above. Your public key will be "
                                        f" pulled automatically from database`"}

                              ]
            await embed_builder(ctx=ctx, title=title, description=description, data=list_of_values,
                                destination=1, c=Colour.dark_orange())

    @voter.group(aliases=['mng'])
    async def management(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':joystick: __Welcome to Voter Management System __ :joystick: '
            description = "If you have voted for delegate, you can register your public key into the system. " \
                          "It will be appended under your Discord User name. Check for benefits."

            list_of_values = [{"name": ":information_source:  Benefits when registered",
                               "value": f"```1. No more copy pasting of your public key"
                                        f"2. Automatic notifications to DM when payments are sent out\n```"},
                              {"name": ":new: Create new profile",
                               "value": f"```{self.command_string}voter management register <public address>```"},
                              {"name": ":octagonal_sign: Delete profile from system",
                               "value": f"```{self.command_string}voter management remove```"},
                              {"name": ":office_worker:  Review registration details",
                               "value": f"```{self.command_string}voter management me```"}

                              ]
            await embed_builder(ctx=ctx, title=title, description=description, data=list_of_values,
                                destination=1, c=Colour.dark_orange())

    @management.command()
    async def register(self, ctx, public_key: str):
        if not self.bot.voters_manager.check_voter(user_id=int(ctx.author.id)):
            if match(r'^XCA[A-Za-z0-9]{95}$|^XCB[A-Za-z0-9]{107}', public_key) is not None:
                if self.bot.voters_manager.register_voter(user_id=int(ctx.author.id), public_key=public_key):
                    details = f"You have successfully registered yourself into the database."
                    await sys_message(ctx=ctx, details=details, c=Colour.green())
                else:
                    details = f"Something went wrong on the backend. Please try again later. We apologize for " \
                              f"inconvenience"
                    await sys_message(ctx=ctx, details=details, c=Colour.red())
            else:
                details = f"You have provided wrong XCASH public key. Please check again. "
                await sys_message(ctx=ctx, details=details, c=Colour.red())

        else:
            details = f"You have already registered yourself into the system. Please use command. "
            await sys_message(ctx=ctx, details=details, c=Colour.red())

    @management.command()
    async def remove(self, ctx):
        if self.bot.voters_manager.check_voter(user_id=int(ctx.author.id)):
            if self.bot.voters_manager.remove_voter(user_id=int(ctx.author.id)):
                details = f"You have been successfully removed from database. Thank You for your votes and support. " \
                          f"Hope that you will be with us again in future."
                await sys_message(ctx=ctx, details=details, c=Colour.green())
            else:
                details = f"Something went wrong on the backend. Please try again later. We apologize for " \
                          f"inconvenience"
                await sys_message(ctx=ctx, details=details, c=Colour.red())
        else:
            details = f"Record of your profile can not be found in the database."
            await sys_message(ctx=ctx, details=details, c=Colour.red())

    @management.command()
    async def me(self, ctx):
        result = self.bot.voters_manager.get_voter(user_id=ctx.author.id)
        if result:
            profile_info = Embed(title="Profile Details",
                                 description="Below are details on your profile, registered to database")
            profile_info.add_field(name=f'Registered public key',
                                   value=f'```{result["publicKey"]}```',
                                   inline=False)
            await ctx.author.send(embed=profile_info)
        else:
            details = f"Record of your profile could not be found in the database. Please register first."
            await sys_message(ctx=ctx, details=details, c=Colour.red())

    @voter.command(aliases=['p'])
    async def payments(self, ctx, public_address=None):

        if not public_address:
            user_data = self.bot.voters_manager.get_voter(ctx.author.id)
            try:
                public_address = user_data["publicKey"]
            except TypeError:
                public_address = None

        if public_address:
            if match(r'^XCA[A-Za-z0-9]{95}$|^XCB[A-Za-z0-9]{107}', public_address) is not None:
                data = list(reversed(self.xDelegate.public_address_payments(public_address=public_address)))[:4]
                await get_last_payments(ctx=ctx, data=data)

            else:
                await ctx.author.send(content='Wrong public address structure provided ')
        else:
            details = f"Record of your profile could not be found in the database. Please register " \
                      f"first or than provide public key when executing command."
            await sys_message(ctx=ctx, details=details, c=Colour.red())

    @voter.command(aliases=['nfo', 'i'])
    async def state(self, ctx, public_address=None):
        if not public_address:
            user_data = self.bot.voters_manager.get_voter(ctx.author.id)
            try:
                public_address = user_data["publicKey"]
            except TypeError:
                public_address = None

        if public_address:
            if match(r'^XCA[A-Za-z0-9]{95}$|^XCB[A-Za-z0-9]{107}', public_address) is not None:
                data = self.xDelegate.pub_addr_info(pub_addr=public_address)
                await state_info(ctx=ctx, data=data)

            else:
                await ctx.author.send(content='Wrong public address structure provided ')

        else:
            details = f"Record of your profile could not be found in the database. Please register " \
                      f"first or than provide public key when executing command"
            await sys_message(ctx=ctx, details=details, c=Colour.red())


def setup(bot):
    bot.add_cog(VoterCommands(bot))
