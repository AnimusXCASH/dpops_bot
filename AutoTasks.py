from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from cogs.utils.customMessages import global_stats, top_delegates
from operator import itemgetter
from discord import Color, Embed

from datetime import datetime
import json


class AutomaticTasks:
    def __init__(self, dpops_wrapper, bot):
        self.dpops_wrapper = dpops_wrapper
        self.bot = bot

    async def delegate_overall_message(self, delegate_settings: dict, delegate_stats: dict):
        daily_stats = self.bot.get_channel(id=int(delegate_settings["channel"]))
        delegate_daily = Embed(title=f':bar_chart: {delegate_stats["delegate_name"]} Statistics',
                               description=f'Daily delegate snapshot.',
                               colour=Color.blue(),
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
                                 value=f'```{delegate_stats["total_payments"]}```')
        delegate_daily.add_field(name=f':judge: Blocks Verified',
                                 value=f'```{delegate_stats["block_verifier_total_rounds"]}```')

        await daily_stats.send(embed=delegate_daily)

    async def send_dpops_stats(self):
        try:
            print('Getting global stats')
            data = self.bot.dpops_queries.statistics.global_stats()
            delegates_count = len(self.bot.dpops_queries.delegates.get_delegates())
            data["totalDelegates"] = delegates_count
            stats_chn = self.bot.get_channel(id=self.bot.stats_channel_id)
            if not data.get("error"):
                await global_stats(destination=stats_chn, data=data)
            else:
                error = data["error"]
                print(error)
        except Exception:
            print("Error")

    async def delegate_ranks(self):
        all_delegates = self.bot.dpops_queries.delegates.get_delegates()
        print("getting delegates")
        if isinstance(all_delegates, list):
            for delegate in all_delegates:
                delegate["total_vote_count"] = int(delegate["total_vote_count"])

            newlist = sorted(all_delegates, key=itemgetter('total_vote_count'), reverse=True)

            top_10 = newlist[0:10]

            stats_chn = self.bot.get_channel(id=self.bot.stats_channel_id)
            await top_delegates(destination=stats_chn, c=Color.dark_orange(), data=top_10)
        else:
            error = all_delegates["error"]
            print(error)

    async def delegate_last_block_check(self):

        # Obtain settings and values from database as dict
        block_data = self.bot.setting.get_setting(setting_name='new_block')
        if block_data["status"] == 1:

            last_block_found = self.dpops_wrapper.delegate_api.get_last_block_found()[0]
            if not last_block_found.get("error"):
                last_checked_block = int(block_data["value"])  # Get last check height as INT from database
                last_produced_block = int(last_block_found["block_height"])

                if last_produced_block > last_checked_block:
                    print("we have new block")
                    block_channel = self.bot.get_channel(id=int(block_data["channel"]))
                    new_block = Embed(title=f':bricks: New block',
                                      description=f'Height @ ***{int(last_block_found["block_height"]):,}***',
                                      colour=Color.green())
                    new_block.add_field(name=f":date: Time",
                                        value=f"```{datetime.fromtimestamp(int(last_block_found['block_date_and_time']))}```")
                    new_block.add_field(name=f":moneybag: Block Value",
                                        value=f"```{float(last_block_found['block_reward']) / (10 ** 6):,} XCASH```",
                                        inline=False)

                    await block_channel.send(embed=new_block)
                    if self.bot.setting.update_settings_by_dict(setting_name="new_block",
                                                                value={"value": int(
                                                                    last_block_found["block_height"])}):
                        print("Last block marked successfully to db")
                    else:
                        print("there has been an issue when marking latest block in database")
                else:
                    print(f"No new blocks have been found by delegate @ f{datetime.utcnow()}")
            else:
                print(f'Could not get block status check DELEGATE: {last_block_found["error"]}')
        else:
            print("Service for delegate block notifcations turned off")

    async def delegate_daily_snapshot(self):
        """
        Send daily snapshot of the delegate overall performance if activated
        """
        delegate_stats = self.dpops_wrapper.delegate_api.get_stats()
        daily_settings = self.bot.setting.get_setting(setting_name='delegate_daily')
        if daily_settings["status"] == 1:
            if not delegate_stats.get("error"):
                if daily_settings["status"] == 1:
                    await self.delegate_overall_message(delegate_settings=daily_settings, delegate_stats=delegate_stats)
            else:
                print(f'No API response fr delegate daily snapshot {delegate_stats["error"]}')
        else:
            print("Daily snapshots are not included")


def start_tasks(automatic_tasks):
    """
    Starts all tasks in the backgroudn
    :param automatic_tasks: AutomaticTasks class
    :return: scheduler
    """
    scheduler = AsyncIOScheduler()
    print('Started Chron Monitors')
    # scheduler.add_job(automatic_tasks.block_monitor,CronTrigger(hour='02',second='02'), misfire_grace_time=2,
    #                   max_instances=20)
    #
    # TODO update to daily before release
    scheduler.add_job(automatic_tasks.delegate_daily_snapshot,
                      CronTrigger(second='00'), misfire_grace_time=2, max_instances=20)
    #
    # scheduler.add_job(automatic_tasks.delegate_ranks, CronTrigger(hour='02', second='02'), misfire_grace_time=2,
    #                   max_instances=20)
    # scheduler.add_job(automatic_tasks.delegate_last_block_check,
    #                   CronTrigger(minute='02,04,06,08,10,12,14,16,18,20,22,24,26,'
    #                                      '28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58'), misfire_grace_time=2,
    #                   max_instances=20)

    scheduler.start()
    print('Started Chron Monitors : DONE')
    return scheduler
