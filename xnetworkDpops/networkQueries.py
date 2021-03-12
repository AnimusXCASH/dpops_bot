from discord.ext import commands
from discord import Color, Embed
from cogs.utils.customMessages import embed_builder, system_message
from datetime import datetime


class NetworkCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_string = self.bot.get_command_str()
        self.delegates = self.bot.dpops_queries.delegates

    async def top_delegates(self, destination, c, data: list, key, title: str):
        time_of_report = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")

        delegate_ranks = Embed(title=f"Top 10 delegates by {title}",
                               colour=c)
        delegate_ranks.add_field(name=f':calendar: Rankings Date :calendar: ',
                                 value=f'```{time_of_report} UTC```',
                                 inline=True)

        if key == "total_vote_count":
            data = [{"delegate_name": x["delegate_name"], f"{key}": int(x[key]) / (10 ** 6)} for x in data]

        top_three = data[0:3]
        rest = data[3:10]
        count = 1
        for t in top_three:
            if count == 1:
                emoji = ":first_place: "
            elif count == 2:
                emoji = ":second_place: "
            elif count == 3:
                emoji = ":third_place: "

            delegate_ranks.add_field(name=f'{emoji} {t["delegate_name"]}',
                                     value=f'```{t[key]:,}```',
                                     inline=False)
            count += 1

        count = 4
        ranks = ''
        for r in rest:
            ranks += f'{count}. {r["delegate_name"]}\n'
            count += 1

        delegate_ranks.add_field(name='Challengers',
                                 value=f'{ranks}')

        await destination.send(embed=delegate_ranks)

    @staticmethod
    def filter_delegates(data, key, filter=None):
        if filter:
            new_list = [{"delegate_name": x["delegate_name"], f"{key}": int(x[key])} for x in data if
                        float(x[key]) > 0 and x['online_status'] != "false" and x["shared_delegate_status"] == filter]
        else:
            new_list = [{"delegate_name": x["delegate_name"], f"{key}": int(x[key])} for x in data if
                        float(x[key]) > 0 and x['online_status'] != "false"]
        s = sorted(new_list, key=lambda d: d[key], reverse=True)
        return s

    @commands.group()
    async def dpops(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':sos: __Dpops Commands__ :sos: '
            description = f"All available commands to query the DPOPS network"
            list_of_commands = [
                {"name": "Check various rankings",
                 "value": f"```{self.command_string}dpops ranks```"},
            ]
            await embed_builder(ctx=ctx, c=Color.green(), title=title, description=description,
                                list_of_commands=list_of_commands)

    @dpops.group()
    async def ranks(self, ctx):
        if ctx.invoked_subcommand is None:
            title = ':trophy: ranks by category'
            description = f"All available commands to query the DPOPS network"
            list_of_commands = [
                {"name": "Check various rankings",
                 "value": f"```{self.command_string}dpops ranks blocks```"},
                {"name": "Check various rankings",
                 "value": f"```{self.command_string}dpops ranks votes```"},
                {"name": "Check various rankings",
                 "value": f"```{self.command_string}dpops ranks verifier```"},
            ]
            await embed_builder(ctx=ctx, c=Color.green(), title=title, description=description,
                                list_of_commands=list_of_commands)

    @ranks.command()
    async def blocks(self, ctx, filter: str = None):
        if filter:
            filter = filter.lower()
        if filter in ['solo', 'shared'] or not filter:
            data = self.delegates.get_delegates()
            processed = self.filter_delegates(data=data, key="block_producer_total_rounds", filter=filter)
            await self.top_delegates(destination=ctx.author, c=Color.gold(), data=processed,
                                     key="block_producer_total_rounds", title='amount of blocks produced')
        else:
            details = "Filter can be ***solo***, ***shared*** or ***Empty*** "
            await system_message(ctx=ctx, c=Color.red(), title=f'Wrong Filter', error_details=details)

    @ranks.command()
    async def votes(self, ctx, filter: str = None):
        if filter:
            filter = filter.lower()
        if filter in ['solo', 'shared'] or not filter:
            data = self.delegates.get_delegates()
            processed = self.filter_delegates(data=data, key="total_vote_count", filter=filter)
            await self.top_delegates(destination=ctx.author, c=Color.gold(), data=processed, key="total_vote_count",
                                     title='amout of votes')
        else:
            details = "Filter can be ***solo***, ***shared*** or ***Empty*** "
            await system_message(ctx=ctx, c=Color.red(), title=f'Wrong Filter', error_details=details)

    @ranks.command()
    async def verifier(self, ctx, filter: str = None):
        if filter:
            filter = filter.lower()

        if filter in ['solo', 'shared'] or not filter:
            data = self.delegates.get_delegates()
            processed = self.filter_delegates(data=data, key="block_verifier_total_rounds", filter=filter)
            await self.top_delegates(destination=ctx.author, c=Color.gold(), data=processed,
                                     key="block_verifier_total_rounds", title='rounds verifier')
        else:
            details = "Filter can be ***solo***, ***shared*** or ***Empty*** "
            await system_message(ctx=ctx, c=Color.red(), title=f'Wrong Filter', error_details=details)

    @ranks.command()
    async def delegate(self, ctx):
        from pprint import pprint
        delegate_name = self.bot.bot_settings["delegateName"]
        data = self.delegates.get_delegates()

        print("getting vote ranks")
        vote_ranks = "total_vote_count"
        new_list = [{"delegate_name": x["delegate_name"], f"{vote_ranks}": int(x[vote_ranks])} for x in data if
                    int(x[vote_ranks]) > 0 and x["online_status"] != 'false']
        s_vote_ranks = sorted(new_list, key=lambda d: d[vote_ranks], reverse=True)

        location_votes = 0
        delegate_ranks = dict()
        for d in s_vote_ranks:
            location_votes += 1
            if d["delegate_name"] == delegate_name:
                delegate_ranks["votes"] = location_votes

        print("Getting block producer ranks")
        block_ranks = "block_producer_total_rounds"
        new_list = [{"delegate_name": x["delegate_name"], f"{block_ranks}": int(x[block_ranks])} for x in data if
                    int(x[block_ranks]) > 0 and x["online_status"] != 'false']
        s_block_ranks = sorted(new_list, key=lambda d: d[block_ranks], reverse=True)

        location_blocks = 0
        for d in s_block_ranks:
            location_blocks += 1
            if d["delegate_name"] == delegate_name:
                delegate_ranks["blocks"] = location_blocks

        print("Getting block verifier ranks")
        verifier_ranks = "block_verifier_total_rounds"
        new_list = [{"delegate_name": x["delegate_name"], f"{verifier_ranks}": int(x[verifier_ranks])} for x in data if
                    int(x[verifier_ranks]) > 0 and x["online_status"] != 'false']
        s_verifier_ranks = sorted(new_list, key=lambda d: d[verifier_ranks], reverse=True)

        location_verifier = 0
        for d in s_verifier_ranks:
            location_verifier += 1
            if d["delegate_name"] == delegate_name:
                delegate_ranks["verifier"] = location_verifier

        pprint(delegate_ranks)


def setup(bot):
    bot.add_cog(NetworkCommands(bot))
