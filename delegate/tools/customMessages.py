from discord import Embed, Colour
from datetime import datetime


async def embed_builder(ctx, title, description, data: list, destination=None, thumbnail=None, c: Colour = None):
    """
    Build embed from data provided
    :param ctx: Discord Context
    :param title: Title for embed
    :param description: Description of embed
    :param data: data as list of dict
    :param destination: where embed is sent
    :param thumbnail: where embed is sent
    :return:
    """

    if not c:
        c = Colour.gold()

    embed = Embed(title=title,
                  description=description,
                  colour=c)
    for d in data:
        embed.add_field(name=d['name'],
                        value=d['value'],
                        inline=False)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    try:
        if destination:
            await ctx.author.send(embed=embed)
        else:
            await ctx.channel.send(embed=embed, delete_after=40)
    except Exception:
        await ctx.channel.send(embed=embed)


async def delegate_stats(destination, data: dict, thumbnail, delegate_name: str):
    """:param
            {
             'total_xcash_from_blocks_found': '2472432078918'}
     """
    data_embed = Embed(title=f'{data["delegate_name"]} Stats',
                       description=f"Current statistics about {delegate_name} delegate operating on ***{round(float(data['fee']), 2)}%*** fee"
                                   f" and minimum payment amount ***{int(data['minimum_amount']):,}*** XCASH.",
                       colour=Colour.green(),
                       timestamp=datetime.utcnow())
    data_embed.set_thumbnail(url=thumbnail)
    data_embed.add_field(name=f':first_place: Rank',
                         value=f'```{data["current_delegate_rank"]}```')
    data_embed.add_field(name=f':timer: Online Percentage',
                         value=f'```{data["online_percentage"]}%```')
    data_embed.add_field(name=f':cowboy: Total Voters',
                         value=f'```{data["total_voters"]}```')
    data_embed.add_field(name=f':ballot_box: Total Votes',
                         value=f'```{int(float(data["total_votes"]) / (10 ** 6)):,} XCASH```')
    data_embed.add_field(name=f':pick: Total XCASH',
                         value=f'```{int(float(data["total_xcash_from_blocks_found"]) / (10 ** 6)):,} XCASH```')
    data_embed.add_field(name=f':incoming_envelope: Total Payments',
                         value=f'```{data["total_payments"]}```')
    data_embed.add_field(name=f':bricks: Blocks Found',
                         value=f'```{data["total_blocks_found"]}```')
    data_embed.add_field(name=f':judge: Blocks Verified',
                         value=f'```{data["block_verifier_total_rounds"]}```')
    await destination.send(embed=data_embed)


async def get_last_blocks(destination, blocks: list, thumbnail):
    block_data = Embed(title=f':bricks: Last 5 blocks produced ',
                       description="Time is set to UTC.",
                       colour=Colour.green())
    block_data.set_thumbnail(url=thumbnail)
    new_block_list = blocks[-5:]
    for b in reversed(new_block_list):
        print(b["block_date_and_time"])
        block_data.add_field(name=f':timer: {datetime.fromtimestamp(int(b["block_date_and_time"]))}',
                             value=f'```Height: {int(b["block_height"]):,}\n'
                                   f'Reward: {int(int(b["block_reward"]) / (10 ** 6)):,} XCASH```',
                             inline=False)

    await destination.send(embed=block_data)


async def get_last_payments(ctx, data: list):
    payments_info = Embed(title='Last 4 payments',
                          colour=Colour.green())
    for p in data:
        payments_info.add_field(name=f':calendar: {datetime.fromtimestamp(int(p["date_and_time"]))}',
                                value=f':money_with_wings:  `{round(int(p["total"]) / (10 ** 6), 6):,} XCASH`\n'
                                      f':hash: `{p["tx_hash"]}`',
                                inline=False)

    await ctx.author.send(embed=payments_info)


async def state_info(ctx, data: dict, xcash_price_usdt: dict):
    try:
        current_pending = round(int(data["current_total"]) / (10 ** 6), 2)
    except  Exception:
        current_pending = 0

    state_nfo = Embed(title=':map: State of voter',
                      description=f"```{data['public_address']}```",
                      colour=Colour.green())

    if xcash_price_usdt.get("USD"):
        try:
            micro = current_pending
            penny = xcash_price_usdt["USD"]
            usd_final = round((micro * penny), 4)
            total_payed = int(data["total"]) / (10 ** 6)
            total_usd_payed_final = round(total_payed * penny, 4)
        except ZeroDivisionError:
            usd_final = 0.00
            total_usd_payed_final = 0.00

    state_nfo.add_field(name=':hourglass_flowing_sand: Current Pending',
                        value=f':coin: `{current_pending:,} XCASH` \n:flag_us: `${usd_final}`')

    state_nfo.add_field(name=':moneybag: Total Payed ',
                        value=f':coin: `{round(int(data["total"]) / (10 ** 6), 6):,}XCASH`\n'
                              f':flag_us: `${total_usd_payed_final:,}`')

    await ctx.author.send(embed=state_nfo)


async def sys_message(ctx, details, c):
    sys_message = Embed(title=':robot: System Message',
                        colour=c)
    sys_message.add_field(name=f'Message',
                          value=f'{details}')

    await ctx.author.send(embed=sys_message)
