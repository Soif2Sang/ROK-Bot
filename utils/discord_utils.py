import discord
import asyncio
from utils.Task_utils import FileSingleton

token = 'MTEwMDM2MTgyNTQ0MDIzOTY3Ng.Gvz3U-.cjhCXxzLs4kNjlqnaZiwJm55-yHRUjKW6oxMks'
user_id = 1018570484977238026

async def send_discord_message(message):
    file_Manager = FileSingleton()
    data = file_Manager.get_data()

    intents = discord.Intents.default()
    intents.messages = True  # Enable the messages intent

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            user = await client.fetch_user(user_id)
            if user:
                await user.send(message)
                print(f"Message sent to user {user.name} ({user.id})")
            else:
                print(f"User with ID {user_id} not found!")

            await client.close()

        except discord.LoginFailure:
            print("Invalid token. Failed to log in.")
        except discord.HTTPException as e:
            print(f"Failed to send the message: {e}")

    await client.start(token)

# Run the async function
