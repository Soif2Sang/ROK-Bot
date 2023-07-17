import time

import discord
from discord.ext import commands

token = 'MTEwMDM2MTgyNTQ0MDIzOTY3Ng.Gvz3U-.cjhCXxzLs4kNjlqnaZiwJm55-yHRUjKW6oxMks'
channel_id = 1039266187311321158 #j'ai oublié
channel_id = 1125159145671237682 #title channel

client = discord.Client(intents=discord.Intents.default())

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

duke_list = []
archi_list = []
scientist_list = []

@client.event
async def on_ready():
    print('Bot is ready!')


async def send_new_update(channel_id):
    channel = await client.fetch_channel(channel_id)
    embed = discord.Embed(
        title='**New UPDATE**',
        description="""

    A new update for the BOT is now available. You can download the latest version [here](https://www.mediafire.com/file/v9rrym9kc26osz2/bot-2023-06-24.exe/file).

    Here are the key features and bug resolutions included in this update:

    - Fixing bug related to the new experimental feature in gather gems.

    Thank you for continuing to use my BOT and enjoy the enhancements brought by this new version!
    """

        ,
        color=discord.Color.blue()
    )
    result = await channel.send(embed=embed)

@bot.command()
async def duke(ctx, kd: str, x: int, y: int):
    user = ctx.author
    duke_list.append({
        'user_id': user.id,
        'username': str(user),
        'kd': kd,
        'x': x,
        'y': y,
        'time': time.time()
    })
    await ctx.send(f'{user.mention} has been added to the list.')

@bot.command()
async def done(ctx):
    user = ctx.author
    for element in 
    await ctx.send(f'{user.mention} has been added to the list.')


@client.event
async def on_connect():
    # channel = client.get_channel(channel_id)
#     channel = await client.fetch_channel(channel_id)
#     embed = discord.Embed(
#         title='**New UPDATE**',
#         description="""
#
# A new update for the BOT is now available. You can download the latest version [here](https://www.mediafire.com/file/v9rrym9kc26osz2/bot-2023-06-24.exe/file).
#
# Here are the key features and bug resolutions included in this update:
#
# - Fixing bug related to the new experimental feature in gather gems.
#
# Thank you for continuing to use my BOT and enjoy the enhancements brought by this new version!
# """
#
# ,
#         color=discord.Color.blue()
#     )
#     result = await send_new_update(channel_id)
#     print(result)
    return



client.run(token)
