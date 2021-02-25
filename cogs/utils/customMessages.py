from discord import Embed, Color
from datetime import datetime


async def embed_builder(ctx, c, title: str, description: str, list_of_commands: list):
    """
    Builds embed from list of dictionaries
    :param ctx: Discord Context to get access to destination
    :param c: discord.Colour
    :param title: Title for embed
    :param description: Description of he embed
    :param list_of_commands: List of commands details as dictionary
    :return: Constructed embed to Discord user DM
    """
    builder_embed = Embed(title=title,
                          description=description,
                          colour=c)
    for d in list_of_commands:
        builder_embed.add_field(name=d['name'],
                                value=d['value'],
                                inline=False)

    await ctx.author.send(embed=builder_embed)


async def top_delegates(destination, c, data: list):
    time_of_report = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")

    delegate_ranks = Embed(title="Top 10 delegates by votes",
                           colour=c)
    delegate_ranks.add_field(name=f':calendar: Rankings Date :calendar: ',
                             value=f'```{time_of_report} UTC```',
                             inline=True)
    top_three = data[0:3]
    rest = data[3:]
    count = 1
    for t in top_three:
        if count == 1:
            emoji = ":first_place: "
        elif count == 2:
            emoji = ":second_place: "
        elif count == 3:
            emoji = ":third_place: "
        delegate_ranks.add_field(name=f'{emoji} {t["delegate_name"]} {emoji}',
                                 value=f'```Votes: {t["total_vote_count"]:,}\n'
                                       f'Producer: {t["block_producer_total_rounds"]}\n'
                                       f'Verifier: {t["block_verifier_total_rounds"]}\n'
                                       f'Online: {t["block_verifier_online_percentage"]}%```',
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


async def system_message(ctx, c, title: str, error_details: str, destination = None):
    """
    System  message to user
    :param ctx: Discord Context to get access to destination
    :param c: discord.Colour
    :param title: Title of system message
    :param error_details: Error details for user
    :return: Information Embed to users DM
    """
    sys_msg = Embed(title=title,
                    colour=c)
    sys_msg.add_field(name=f'Message',
                      value=f'{error_details}')
    if not destination:
        await ctx.author.send(embed=sys_msg)
    else:
        await destination.send(embed=sys_msg)


async def global_stats(destination, data: dict, vote_recount: bool = None):
    """
    Global DPOPS stats embed
    :param destination: discord.Channel / discord.User
    :param data: Data from API
    :return: Embed to Discord
    """
    time_of_report = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")

    global_stats = Embed(title=':bar_chart: DPOPS statistics :bar_chart:',
                         description=f'Current Round Number ***{data["XCASH_DPOPS_round_number"]}***',
                         colour=Color.orange())
    global_stats.add_field(name=f':calendar: Time of report :calendar: ',
                           value=f'```{time_of_report} UTC```',
                           inline=True)

    if vote_recount:
        # New recalculation of votes
        current_time = datetime.utcnow()

        global_stats.set_footer(
            text=f'Next recalculating of votes after {59 - current_time.minute}:{59 - current_time.second}')

    global_stats.add_field(name=f':family_man_boy_boy: Total Delegates :family_man_boy_boy: ',
                           value=f'```{data["totalDelegates"]}```',
                           inline=False)
    global_stats.add_field(name=':hash: Current Block Height :hash: ',
                           value=f'```{int(data["current_block_height"]):,}```',
                           inline=True)
    global_stats.add_field(name=':arrows_counterclockwise: DPOPS circulating :arrows_counterclockwise: ',
                           value=f'```{data["XCASH_DPOPS_circulating_percentage"]}%```',
                           inline=True)
    global_stats.add_field(name=':inbox_tray: Total Votes :inbox_tray: ',
                           value=f'```{int(data["total_votes"]):,}```',
                           inline=False)
    global_stats.add_field(name=':hammer_pick: Best by blocks produced :hammer_pick: ',
                           value=f'```Delegate: {data["most_block_producer_total_rounds_delegate_name"]}\n'
                                 f'∑ blocks: {data["most_block_producer_total_rounds"]} blocks```',
                           inline=False)
    global_stats.add_field(name=':repeat: Best by total rounds :repeat: ',
                           value=f'```Delegate: {data["most_total_rounds_delegate_name"]}\n'
                                 f'∑ rounds: {data["most_total_rounds"]} rounds```',
                           inline=False)
    global_stats.add_field(name=':abacus: Best by producer/verifier ratio:abacus: ',
                           value=f'```Delegate: {data["best_block_verifier_online_percentage_delegate_name"]}\n'
                                 f'Ratio: {data["best_block_verifier_online_percentage"]}%```',
                           inline=False)

    await destination.send(embed=global_stats)

