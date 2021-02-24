from discord import ChannelType


def is_owner(ctx):
    try:
        return int(ctx.message.author.id) == int(ctx.message.guild.owner.id)
    except AttributeError:
        return False


def is_public(ctx):
    try:
        return ctx.message.channel.type != ChannelType.private
    except AttributeError:
        return False
