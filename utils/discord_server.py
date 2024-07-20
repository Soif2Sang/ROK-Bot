import threading

import cv2
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from tasks.Worker_runner import WorkerRunner
from utils.context import contextManager
from utils.schemas.discord_schemas import DiscordWorkerListSingleton

load_dotenv()


def start_server():
    # Replace these values with your own
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents)

    discord_settings = DiscordWorkerListSingleton()


    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')


    @bot.event
    async def on_message(message):
        # Check if the message is from the specified user in the specified channel
        for worker in discord_settings.read_worker_list().workers:
            if message.channel.id == int(worker.channel_id) and message.author.id == int(worker.discord_id):
                content = message.content.lower()

                if content == 'start':
                    await message.channel.send('Start command received!')
                    # contextManager.start(worker.worker, WorkerRunner(worker.worker))
                    # Add your start command handling logic here
                    if contextManager.tasks.get(worker.worker) and contextManager.tasks.get(worker.worker).status == "running":
                        await message.channel.send('Task is already running.')
                        return

                    threading.Thread(target=contextManager.get_worker(worker.worker).start, args=(None,)).start()


                elif content == 'stop':
                    await message.channel.send('Stop command received!')
                    # contextManager.stop(worker.worker)
                    if not contextManager.tasks.get(worker.worker) or contextManager.tasks.get(worker.worker).status != "running":
                        await message.channel.send('No task is running for this worker.')
                        return

                    contextManager.get_worker(worker.worker).stop(None)

                    # Add your stop command handling logic here

                elif content == 'show':
                    await message.channel.send('Show command received!')

                    if not contextManager.tasks.get(worker.worker) or  contextManager.tasks.get(worker.worker).status != "running":
                        await message.channel.send('No task is running for this worker.')
                        return

                    screen = WorkerRunner(worker.worker, contextManager, 'ld').get_screen()
                    path = f'screen_{worker.worker}.png'
                    cv2.imwrite(path, screen)

                    embed = discord.Embed(title=f"Game screen")
                    file = discord.File(path, filename=path)
                    embed.set_image(url="attachment://" + path)
                    await message.channel.send(embed=embed, file=file)
                    # Add your show command handling logic here

            await bot.process_commands(message)


    # Start the bot
    bot.run(DISCORD_BOT_TOKEN)
