from discord.ext import commands
from delegate.tools.customMessages import embed_builder, delegate_stats, get_last_blocks, get_last_payments, state_info, \
    sys_message
from datetime import datetime
from discord import Colour, Embed
from re import match
import time


class VoterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()
        self.delegate_api_access = self.bot.dpops_queries.delegate_api

    @staticmethod
    def get_status_number(status: str):
        if status == 'on':
            return 1
        elif status == 'off':
            return 0

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
                              {"name": ":mega: Apply for available automatic notifications",
                               "value": f"```{self.command_string}voter notify```"},
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

    @voter.group()
    async def notify(self, ctx):
        if ctx.invoked_subcommand is None:
            title = 'Automatic notifications system'
            description = "Bellow are all availabale services which allow you to apply your registered public key " \
                          "to be monitored for various activities. "

            list_of_values = [{"name": ":money_with_wings: Get notifications to DM when delegate sends you payment",
                               "value": f"```{self.command_string}voter notify reward <on/off>```"}

                              ]
            await embed_builder(ctx=ctx, title=title, description=description, data=list_of_values,
                                destination=1, c=Colour.dark_orange())

    @notify.group()
    async def reward(self, ctx, status: str):
        status = status.lower()
        if self.bot.voters_manager.check_voter(ctx.author.id):
            if status and status in ["on", "off"]:
                status_code = self.get_status_number(status=status)
                voter_details = self.bot.voters_manager.get_voter(ctx.author.id)
                public_address = voter_details["publicKey"]

                get_payments = self.bot.dpops_queries.delegate_api.public_address_payments(
                    public_address=public_address)
                # Check if not error in the returned == some payments have been done already
                if not get_payments.get("error"):
                    payments = list(reversed(get_payments))[:1]
                    last_one = payments[0]
                else:
                    last_one = {"date_and_time": int(time.time())}

                if self.bot.voters_manager.update_payment_notification_status(user_id=ctx.author.id, status=status_code,
                                                                              timestamp=last_one["date_and_time"]):
                    details = f"You have successfully activate automatic payment notifications. Bot will send you " \
                              f"DM when payment is processed. Please make sure as well that bot can contact you over " \
                              f"DM otherwise message will not come through."
                    await sys_message(ctx=ctx, details=details, c=Colour.green())

                    if status == "on":
                        if not get_payments.get("error"):
                            last_sent_payment = Embed(title=":incoming_envelope: Last Payment",
                                                      description="Details of last payment sent from delegate",
                                                      colour=Colour.green())
                            last_sent_payment.set_author(name=f'{self.bot.user}')
                            last_sent_payment.set_thumbnail(url=self.bot.user.avatar_url)
                            last_sent_payment.add_field(name=f':calendar: Time Of payment',
                                                        value=f'{datetime.fromtimestamp(int(last_one["date_and_time"]))}')
                            last_sent_payment.add_field(name=f':money_with_wings: Xcash Amount',
                                                        value=f'`{round(int(last_one["total"]) / (10 ** 6), 6):,} XCASH`')
                            last_sent_payment.add_field(name=f':hash:Transaction Hash',
                                                        value=f'```{last_one["tx_hash"]}```',
                                                        inline=False)
                            last_sent_payment.add_field(name=f':key: Transaction Key',
                                                        value=f'```{last_one["tx_key"]}```',
                                                        inline=False)
                            last_sent_payment.set_footer(text='Thank you for voting!')
                            await ctx.author.send(embed=last_sent_payment)
                        else:
                            last_sent_payment = Embed(title=":incoming_envelope: Last Payment",
                                                      description="Details of last payment sent from delegate",
                                                      colour=Colour.green())
                            last_sent_payment.set_author(name=f'{self.bot.user}')
                            last_sent_payment.set_thumbnail(url=self.bot.user.avatar_url)
                            last_sent_payment.add_field(name=f":warning: Message",
                                                        value=f'Delegate has no marked payments yet under the provided/'
                                                              f'registered public key. Notification will be sent to '
                                                              f'your DM as soon as first payment is processed. Please '
                                                              f' allow private messages for the bot. ')
                            last_sent_payment.set_footer(text='Thank you for voting!')
                            await ctx.author.send(embed=last_sent_payment)
                    else:
                        last_sent_payment = Embed(title=":incoming_envelope: Reward Notifications",
                                                  colour=Colour.green())
                        last_sent_payment.set_author(name=f'{self.bot.user}')
                        last_sent_payment.set_thumbnail(url=self.bot.user.avatar_url)
                        last_sent_payment.add_field(name=f"Message",
                                                    value=f'You have successfully turned OFF automatic notifications, '
                                                          f'when rewards are distributed to you by the delegate.')
                        last_sent_payment.set_footer(text='Thank you for voting!')
                        await ctx.author.send(embed=last_sent_payment)

                else:
                    details = "It seems like there haas been a backend issue. Please try again later or open github " \
                              "ticket and let us know."
                    await sys_message(ctx=ctx, c=Colour.red(), details=details)
            else:
                details = f"You have provided wrong status. Available are ***on/off*** while yours was {status}"
                await sys_message(ctx=ctx, c=Colour.red(), details=details)
        else:
            details = f"You can not apply to automatic payment notifications, because you have not registered " \
                      f"yourself yet into the system. Execute ***{self.command_string} voter management register " \
                      f"<public key used for voting>***"
            await sys_message(ctx=ctx, details=details, c=Colour.red())

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
                get_payments = self.delegate_api_access.public_address_payments(public_address=public_address)
                if isinstance(get_payments, list):
                    data = list(reversed(get_payments))[:4]
                    await get_last_payments(ctx=ctx, data=data)
                else:
                    last_payments = Embed(title=":incoming_envelope: Reward Notifications",
                                          colour=Colour.green())
                    last_payments.set_author(name=f'{self.bot.user}')
                    last_payments.set_thumbnail(url=self.bot.user.avatar_url)
                    last_payments.add_field(name=f":warning: Message",
                                            value=f'You have not received any payments yet from delegate.')
                    last_payments.set_footer(text='Thank you for voting!')
                    await ctx.author.send(embed=last_payments)
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
                data = self.delegate_api_access.pub_addr_info(pub_addr=public_address)
                if not data.get("error"):
                    await state_info(ctx=ctx, data=data,xcash_price_usdt=self.bot.dpops_queries.xcash_explorer.price())
                else:
                    last_payments = Embed(title=":map: State Information",
                                          colour=Colour.green())
                    last_payments.set_author(name=f'{self.bot.user}')
                    last_payments.set_thumbnail(url=self.bot.user.avatar_url)
                    last_payments.add_field(name=f":warning: Message",
                                            value=f'No information could be obtained currently on public key '
                                                  f' `{public_address}`. Please try again later. ')
                    last_payments.set_footer(text='Thank you for voting!')
                    await ctx.author.send(embed=last_payments)

            else:
                await ctx.author.send(content='Wrong public address structure provided ')

        else:
            details = f"Record of your profile could not be found in the database. Please register " \
                      f"first or than provide public key when executing command"
            await sys_message(ctx=ctx, details=details, c=Colour.red())


def setup(bot):
    bot.add_cog(VoterCommands(bot))
