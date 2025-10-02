import os
import discord
from dotenv import load_dotenv
from responses import get_response

#LOAD TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#BOT SETUP
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#SEND MESSAGES
async def send_message(message, user_message) -> None:
    if not user_message:
        print("Message was empty because intents were not enabled")
        return
    
    try:
        response: str = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)

#BOT STARTUP
@client.event
async def on_ready() -> None:
    print(f"Every second you're not running, {client.user.display_name} is getting closer...")

#HANDLE INCOMING MESSAGES
@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)

    print(f"{username} said \"{user_message}\" in {channel}")
    await send_message(message, user_message)

#MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()