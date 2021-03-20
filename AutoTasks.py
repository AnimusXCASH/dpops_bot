from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from xcash_wallet.xcash import XcashManager
from discord import Colour, Embed
import tweepy
from datetime import datetime
import random


class AutomaticTasks:
    def __init__(self, dpops_wrapper, bot):
        self.xcash_manager = XcashManager()
        self.dpops_wrapper = dpops_wrapper
        self.bot = bot
        self.command_string = self.bot.get_command_str()
        self.twitter_credentials = self.bot.bot_settings['twitter']
        if self.twitter_credentials["status"]:
            auth = tweepy.OAuthHandler(self.twitter_credentials["apiKey"], self.twitter_credentials["apiSecret"])
            auth.set_access_token(self.twitter_credentials["accessToken"], self.twitter_credentials["accessSecret"])
            self.twitter_messages = tweepy.API(auth)
        else:
            self.twitter_messages = None

    @staticmethod
    def produce_hash_tag_list():
        hashtag_list = ["#dpops", "#weareXCASH", "$xcash", "#xcash", "#xcashians", "#xcashian", "#crypto",
                        "#cryptocurrency", "#blockchain", "#trading", "#fintech", "#bitcoin", "#monero", "#xmr"]

        random_hash_string = random.sample(hashtag_list, 3)
        hash_list = ' '.join(random_hash_string)
        return hash_list

    def tweet_service_status(self, setting_name: str):
        twitter_notifications = self.bot.setting.get_setting(setting_name=setting_name)
        if twitter_notifications["status"] == 1:
            return True
        else:
            return False

    def tweet(self, text):
        try:
            self.twitter_messages.update_status(text)
        except Exception as e:
            print(f'Could not dispatch Twitter message due to {e}')
            pass

    async def vote_marketing_tweet(self):
        """
        Send message to twitter with voting initiative
        """
        print("Vote marketing")
        if self.twitter_messages and self.tweet_service_status(setting_name="t_call_to_vote"):
            print("Sending tweet")
            self.tweet(
                text=f'Vote for delegate with --> {self.bot.bot_settings["voteString"]} {self.produce_hash_tag_list()}')

    async def delegate_overall_message(self, delegate_settings: dict, delegate_stats: dict, description: str):
        daily_stats = self.bot.get_channel(id=int(delegate_settings["channel"]))
        delegate_daily = Embed(title=f':bar_chart: {delegate_stats["delegate_name"]} Statistics',
                               description=f'{description}',
                               colour=Colour.blue(),
                               timestamp=datetime.utcnow())
        delegate_daily.add_field(name=f':medal: Delegate Rank',
                                 value=f'```{delegate_stats["current_delegate_rank"]}```')
        delegate_daily.add_field(name=f':timer: Online Percentage',
                                 value=f'```{delegate_stats["online_percentage"]}%```')
        delegate_daily.add_field(name=f':cowboy: Total Voters',
                                 value=f'```{delegate_stats["total_voters"]}```')
        delegate_daily.add_field(name=f':ballot_box: Total Votes',
                                 value=f'```{round(int(delegate_stats["total_votes"]) / (10 ** 6), 2):,}```')
        delegate_daily.add_field(name=f':pick: Total XCASH',
                                 value=f'```{round(int(delegate_stats["total_xcash_from_blocks_found"]), 6) / (10 ** 6):,} XCASH```')
        delegate_daily.add_field(name=f':incoming_envelope:  Total Payments',
                                 value=f'```{delegate_stats["total_payments"]}```')
        delegate_daily.add_field(name=f':bricks: Blocks Found',
                                 value=f'```{delegate_stats["total_blocks_found"]}```')
        delegate_daily.add_field(name=f':judge: Blocks Verified',
                                 value=f'```{delegate_stats["block_verifier_total_rounds"]}```')

        await daily_stats.send(embed=delegate_daily)

    async def delegate_last_block_check(self):
        # Obtain settings and values from database as dict
        block_data = self.bot.setting.get_setting(setting_name='new_block')
        if block_data["status"] == 1:
            response = self.dpops_wrapper.delegate_api.get_last_block_found()
            if isinstance(response, list):
                new_block_list = response[-1:]
                last_block_found = new_block_list[0]

                last_checked_block = int(block_data["value"])  # Get last check height as INT from database
                last_produced_block = int(last_block_found["block_height"])
                if last_produced_block > last_checked_block:
                    print("we have new block")
                    # Get the price of xcash on market
                    xcash_value = self.bot.dpops_queries.xcash_explorer.price()
                    if xcash_value.get("USD"):
                        xcash_usd = xcash_value["USD"]
                    else:
                        xcash_usd = 0.0

                    xcash_block_size = float(last_block_found['block_reward']) / (10 ** 6)
                    usd_final = round((xcash_block_size * xcash_usd), 4)

                    block_channel = self.bot.get_channel(id=int(block_data["channel"]))
                    new_block = Embed(title=f':bricks: New block',
                                      description=f'Height @ ***{int(last_block_found["block_height"]):,}***',
                                      colour=Colour.green())
                    new_block.add_field(name=f":date: Time",
                                        value=f"```{datetime.fromtimestamp(int(last_block_found['block_date_and_time']))}```")
                    new_block.add_field(name=f":moneybag: Block Value",
                                        value=f":coin: `{xcash_block_size:,} XCASH`\n"
                                              f":flag_us: `${usd_final}`",
                                        inline=False)

                    await block_channel.send(embed=new_block)

                    if self.twitter_messages and self.tweet_service_status(setting_name="t_new_block"):
                        self.tweet(text=f"New block produced @ height {int(last_block_found['block_height']):,} "
                                        f" in value of {xcash_block_size:,} XCASH (${usd_final})"
                                        f" {self.produce_hash_tag_list()}")

                    if self.bot.setting.update_settings_by_dict(setting_name="new_block",
                                                                value={"value": int(
                                                                    last_block_found["block_height"])}):
                        print("Last block marked successfully to db")
                    else:
                        print("there has been an issue when marking latest block in database")

                else:
                    print(f"No new blocks have been found by delegate @ f{datetime.utcnow()}")

            else:
                print(f"{response['error']}")

    async def delegate_daily_snapshot(self):
        """
        Send daily snapshot of the delegate overall performance if activated
        """
        daily_settings = self.bot.setting.get_setting(setting_name='delegate_daily')
        if daily_settings["status"] == 1:
            delegate_stats = self.dpops_wrapper.delegate_api.get_stats()
            if not delegate_stats.get("error"):

                await self.delegate_overall_message(delegate_settings=daily_settings, delegate_stats=delegate_stats,
                                                    description='Daily Delegate Snapshot')

                # Twitter message for daily
                if self.twitter_messages and self.tweet_service_status(setting_name="t_del_daily"):
                    print("sending daily stats to twitter")
                    conversion_xcash = int(int(delegate_stats['total_xcash_from_blocks_found']) / (10 ** 6))
                    in_millions = int(conversion_xcash / (10 ** 6))

                    self.tweet(text=f"24h Stats {self.bot.bot_settings['delegateName']}\n"
                                    f"Rank: {delegate_stats['current_delegate_rank']}\n"
                                    f"Blocks Found: {delegate_stats['total_blocks_found']}\n"
                                    f"Produced: {in_millions} Mil XCASH\n"
                                    f"Total Voters: {delegate_stats['total_voters']}\n"
                                    f"{self.produce_hash_tag_list()}")
            else:
                print(f'No API response fr delegate daily snapshot {delegate_stats["error"]}')
        else:
            print("Daily snapshots deactivated")

    async def delegate_hourly_snapshots(self):
        """
        Send daily snapshot of the delegate overall performance if activated
        """
        hourly_settings = self.bot.setting.get_setting(setting_name='delegate_hourly')
        if hourly_settings["status"] == 1:
            delegate_stats = self.dpops_wrapper.delegate_api.get_stats()
            if not delegate_stats.get("error"):
                if hourly_settings["status"] == 1:
                    await self.delegate_overall_message(delegate_settings=hourly_settings,
                                                        delegate_stats=delegate_stats,
                                                        description='Hourly Delegate Snapshot'
                                                        )
            else:
                print(f'No API response fr delegate daily snapshot {delegate_stats["error"]}')
        else:
            print("1h snapshot deactivated")

    async def delegate_3_h(self):
        """
        Send snapshot to channel every 3H
        """
        settings = self.bot.setting.get_setting(setting_name='delegate_3h')
        if settings["status"] == 1:
            delegate_stats = self.dpops_wrapper.delegate_api.get_stats()
            if not delegate_stats.get("error"):
                if settings["status"] == 1:
                    await self.delegate_overall_message(delegate_settings=settings,
                                                        delegate_stats=delegate_stats,
                                                        description='3 H Delegate Snapshot'
                                                        )
            else:
                print(f'No API response fr delegate daily snapshot {delegate_stats["error"]}')
        else:
            print("3h snapshot deactivated")

    async def delegate_4_h(self):
        """
        Send snapshot to channel every 4H
        """
        settings = self.bot.setting.get_setting(setting_name='delegate_4h')
        if settings["status"] == 1:
            delegate_stats = self.dpops_wrapper.delegate_api.get_stats()
            if not delegate_stats.get("error"):
                if settings["status"] == 1:
                    await self.delegate_overall_message(delegate_settings=settings,
                                                        delegate_stats=delegate_stats,
                                                        description='4 H Delegate Snapshot'
                                                        )
            else:
                print(f'No API response fr delegate daily snapshot {delegate_stats["error"]}')
        else:
            print("4h snapshot deactivated")

    async def delegate_6_h(self):
        """
        Send snapshot to channel every 6H
        """
        settings = self.bot.setting.get_setting(setting_name='delegate_6h')
        if settings["status"] == 1:
            delegate_stats = self.dpops_wrapper.delegate_api.get_stats()
            if not delegate_stats.get("error"):
                if settings["status"] == 1:
                    await self.delegate_overall_message(delegate_settings=settings,
                                                        delegate_stats=delegate_stats,
                                                        description='6 H Delegate Snapshot'
                                                        )
            else:
                print(f'No API response fr delegate daily snapshot {delegate_stats["error"]}')
        else:
            print("6h snapshot deactivated")

    async def delegate_12_h(self):
        """
        Send snapshot to channel every 12H
        """
        settings = self.bot.setting.get_setting(setting_name='delegate_12h')
        if settings["status"] == 1:
            delegate_stats = self.dpops_wrapper.delegate_api.get_stats()
            if not delegate_stats.get("error"):
                if settings["status"] == 1:
                    await self.delegate_overall_message(delegate_settings=settings,
                                                        delegate_stats=delegate_stats,
                                                        description='12 H Delegate Snapshot'
                                                        )
            else:
                print(f'No API response fr delegate daily snapshot {delegate_stats["error"]}')
        else:
            print("12h snapshot deactivated")

    async def system_payment_notifications(self):
        payment_notifications = self.bot.setting.get_setting(setting_name='payment_notifications')
        if payment_notifications["status"] == 1:
            rpc_wallet_resp = self.xcash_manager.xcash_rpc_wallet.get_last_outgoing_transfers(
                last_processed_height=payment_notifications["value"])
            if rpc_wallet_resp["result"]:
                new_outgoing = rpc_wallet_resp["result"]["out"]
                payment_channel = self.bot.get_channel(id=int(payment_notifications["channel"]))

                # Get the price of xcash on market
                xcash_value = self.bot.dpops_queries.xcash_explorer.price()
                if xcash_value.get("USD"):
                    xcash_usd = xcash_value["USD"]
                else:
                    xcash_usd = 0.0

                for tx in new_outgoing:
                    xcash_payment_value = float(tx['amount']) / (10 ** 6)
                    usd_final = round((xcash_payment_value * xcash_usd), 4)

                    payments_emb = Embed(title=f':incoming_envelope: I have sent out payments!',
                                         description=f'Use `!voter payments` to check if you have '
                                                     f'been part of the batch.',
                                         colour=Colour.dark_orange())
                    payments_emb.set_thumbnail(url=self.bot.user.avatar_url)
                    payments_emb.add_field(name=f":date: Time",
                                           value=f"`{datetime.fromtimestamp(int(tx['timestamp']))}`")
                    payments_emb.add_field(name=f":bricks: Block Height",
                                           value=f"`{tx['height']}`",
                                           inline=True)
                    payments_emb.add_field(name=f":money_with_wings: Total sent in batch",
                                           value=f":coin: `{float(tx['amount']) / (10 ** 6):,} XCASH`\n"
                                                 f":flag_us: `${usd_final}`",
                                           inline=False)
                    payments_emb.add_field(name=f":id: Transaction ID ",
                                           value=f"```{tx['txid']}```",
                                           inline=False)
                    payments_emb.set_footer(text="Thank you for votes")
                    payments_emb.set_author(name=f'{self.bot.user}', url='http://xpayment.x-network.eu/')
                    await payment_channel.send(embed=payments_emb)
                if self.bot.setting.update_settings_by_dict(setting_name="payment_notifications",
                                                            value={"value": int(new_outgoing[-1]["height"])}):
                    print("db updated successfully")
                else:
                    print("Could not update DB")
            else:
                print("No new payments done")

    async def send_payment_dms(self):
        all_applied = self.bot.backend_manager.voters.payment_notifications_applied()
        xcash_value = self.bot.dpops_queries.xcash_explorer.price()
        if xcash_value.get("USD"):
            xcash_usd = xcash_value["USD"]
        else:
            xcash_usd = 0.0

        for voter in all_applied:
            get_payments = self.bot.dpops_queries.delegate_api.public_address_payments(
                public_address=voter["publicKey"])

            if isinstance(get_payments, list):
                payments = list(reversed(get_payments))[:1]
                last_payment = payments[0]
                if int(last_payment["date_and_time"]) > int(voter["lastProcessed"]):
                    if self.bot.backend_manager.voters.update_payment_notification_status(user_id=voter["userId"],
                                                                                          status=1,
                                                                                          timestamp=int(
                                                                                              last_payment[
                                                                                                  "date_and_time"])):
                        xcash_payment_value = int(last_payment["total"]) / (10 ** 6)
                        usd_final = round((xcash_payment_value * xcash_usd), 4)

                        user_destination = await self.bot.fetch_user(user_id=int(voter["userId"]))
                        last_sent_payment = Embed(title=":incoming_envelope: New payment dispatched",
                                                  description="Delegate has sent you new payment/reward based on your"
                                                              " votes",
                                                  colour=Colour.green())
                        last_sent_payment.set_author(name=f'{self.bot.user}')
                        last_sent_payment.set_thumbnail(url=self.bot.user.avatar_url)
                        last_sent_payment.add_field(name=f':calendar: Time Of payment',
                                                    value=f'{datetime.fromtimestamp(int(last_payment["date_and_time"]))}')
                        last_sent_payment.add_field(name=f':money_with_wings: Xcash Amount',
                                                    value=f':coin:`{round(int(last_payment["total"]) / (10 ** 6), 6):,}'
                                                          f' XCASH`\n :flag_us: `${round(usd_final, 4)}`')
                        last_sent_payment.add_field(name=f':hash:Transaction Hash',
                                                    value=f'```{last_payment["tx_hash"]}```',
                                                    inline=False)
                        last_sent_payment.add_field(name=f':key: Transaction Key',
                                                    value=f'```{last_payment["tx_key"]}```',
                                                    inline=False)
                        last_sent_payment.set_footer(text='Thank you for voting!')
                        try:
                            await user_destination.send(embed=last_sent_payment)
                        except Exception:
                            pass
                    else:
                        print('backend error')


def start_tasks(automatic_tasks, snapshot_times):
    """
    Starts all tasks in the backgroudn
    :param automatic_tasks: AutomaticTasks class
    :return: scheduler
    """
    scheduler = AsyncIOScheduler()
    print('Started Chron Monitors')
    scheduler.add_job(automatic_tasks.vote_marketing_tweet,
                      CronTrigger(hour=12,minute='01'), misfire_grace_time=2,
                      max_instances=20)
    scheduler.add_job(automatic_tasks.delegate_hourly_snapshots,
                      CronTrigger(minute=snapshot_times["delHourly"]["minute"],
                                  second=snapshot_times["delHourly"]["second"]), misfire_grace_time=2,
                      max_instances=20)
    scheduler.add_job(automatic_tasks.delegate_3_h,
                      CronTrigger(hour=snapshot_times["delThreeHour"]["hour"],
                                  minute=snapshot_times["delThreeHour"]["minute"],
                                  second=snapshot_times["delThreeHour"]["second"]),
                      misfire_grace_time=2,
                      max_instances=20)
    scheduler.add_job(automatic_tasks.delegate_4_h,
                      CronTrigger(hour=snapshot_times["delFourHour"]["second"],
                                  minute=snapshot_times["delFourHour"]["minute"],
                                  second=snapshot_times["delFourHour"]["second"]), misfire_grace_time=2,
                      max_instances=20)
    scheduler.add_job(automatic_tasks.delegate_6_h,
                      CronTrigger(hour=snapshot_times["delSixHour"]["hour"],
                                  minute=snapshot_times["delSixHour"]["minute"],
                                  second=snapshot_times["delSixHour"]["minute"]), misfire_grace_time=2,
                      max_instances=20)
    scheduler.add_job(automatic_tasks.delegate_12_h,
                      CronTrigger(hour=snapshot_times["delTwelveHour"]["hour"],
                                  minute=snapshot_times["delTwelveHour"]["minute"],
                                  second=snapshot_times["delTwelveHour"]["second"]), misfire_grace_time=2,
                      max_instances=20)
    scheduler.add_job(automatic_tasks.delegate_daily_snapshot,
                      CronTrigger(hour=snapshot_times["delDaily"]["hour"], minute=snapshot_times["delDaily"]["minute"],
                                  second=snapshot_times["delDaily"]["second"]), misfire_grace_time=2, max_instances=20)
    scheduler.add_job(automatic_tasks.system_payment_notifications,
                      CronTrigger(minute=snapshot_times["delPaymentChk"]["minute"],
                                  second=snapshot_times["delPaymentChk"]["second"]), misfire_grace_time=2,
                      max_instances=20)
    scheduler.add_job(automatic_tasks.send_payment_dms,
                      CronTrigger(minute=snapshot_times["paymentDms"]["minute"],
                                  second=snapshot_times["paymentDms"]["second"]), misfire_grace_time=2,
                      max_instances=20)
    scheduler.add_job(automatic_tasks.delegate_last_block_check,
                      CronTrigger(minute=snapshot_times["paymentDms"]["minute"],
                                  second=snapshot_times["paymentDms"]["minute"]),
                      misfire_grace_time=2,
                      max_instances=20)
    scheduler.start()
    print('Started Chron Monitors : DONE')
    return scheduler
