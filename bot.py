import os
import discord
import random
import asyncio
from dotenv import load_dotenv
from responses import get_response

#LOAD ENVIRONMENT VARIABLES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

#BOT SETUP
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#BOT STARTUP
@client.event
async def on_ready() -> None:
    print(f"{client.user.display_name} is running...")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("*Jaquavius is now running!\nAs you should be. Because every second you're not running, I'm getting closer...*")
    client.loop.create_task(daily_quote())

#SEND A QUOTE PERIODICALLY
async def daily_quote() -> None:
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        delay = random.randint(60 * 60 * 5, 60 * 60 * 10)
        await asyncio.sleep(delay)
        if channel:
            quote = get_response(user_input='quote')
            await channel.send(quote)

#HANDLE INCOMING MESSAGES
@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return

    #Log activity
    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)

    log_message = f"{username} said \"{user_message}\" in {channel}"
    with open("message_log.txt", "a") as log:
        log.write(log_message + "\n")

    #Send message in channel
    await send_message(message, user_message)

    #DM User
    try:
        random_delay = random.randint(0, 500)
        await asyncio.sleep(random_delay)
        await message.author.send("Hi")
    except Exception as e:
        print(e)


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
        
#MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()