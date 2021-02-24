from discord import ChannelType


def is_owner(ctx):
    return int(ctx.message.author.id) == int(ctx.message.guild.owner.id)


def is_public(ctx):
    return ctx.message.channel.type != ChannelType.private
