import discord

token = 'MTEwMDM2MTgyNTQ0MDIzOTY3Ng.Gvz3U-.cjhCXxzLs4kNjlqnaZiwJm55-yHRUjKW6oxMks'
channel_id = 1039266187311321158

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('Bot is ready!')


async def send_new_update():
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
@client.event
async def on_connect():
    # channel = client.get_channel(channel_id)
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
    print(result)

client.run(token)
