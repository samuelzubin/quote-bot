import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from responses import get_response
import bot_commands
import threading
from flask import Flask
import time
import requests
import asyncio
from datetime import timedelta

#LOAD ENVIRONMENT VARIABLES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PING_URL = os.getenv('PING_URL')

#SET UP WEB SERVER
app = Flask(__name__)

@app.route('/')
def home() -> str:
    return "Bot is running!"

def run_web_server() -> None:
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, use_reloader=False, threaded=True)

def ping(url) -> None:
    #Pings flask server to prevent bot from going offline
    while True:
        try:
            requests.get(url)
            print("Pinged web server")
        except Exception as e:
            print("Failed to ping web server:", e)
        time.sleep(10 * 60)  # ping every 10 minutes

class Client(commands.Bot):
    async def on_ready(self):
        #SYNC COMMANDS
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Error syncing commands: {e}")


        print(f"{self.user.display_name} is online!")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        
        if 'jaqua' in message.content.lower():
            delay: float = 0.33

            #Fun message sequence
            msg = await message.channel.send("^_^")
            await asyncio.sleep(delay)
            await msg.edit(content="^0^")
            await asyncio.sleep(delay)
            await msg.edit(content="¬_¬")
            await asyncio.sleep(delay)
            await msg.edit(content="^_^")
            await asyncio.sleep(delay / 2)
            await msg.edit(content="^_~")
            await asyncio.sleep(delay / 2)
            await msg.edit(content="^_^")
            await asyncio.sleep(delay)

            #Reply with quote
            await message.reply(get_response())

            #Delete reaction after some time
            await msg.delete(delay=60)

        #Log messages
        with open("message_log.txt", "a", encoding="utf-8") as log:
            user_message: str = message.content.encode("utf-8", errors="replace").decode("utf-8")  #Handle unknown characters
            message_time: str = (message.created_at - timedelta(hours=7)).strftime('%b %d %H:%M:%S')  #Formate time for UTC-7
            
            if message.guild is None:
                message_location: str = "DM"
            else:
                message_location: str = str(message.guild)

            log.write(f"{message_time}  {message.author} @ {message_location}: {user_message}")
            log.write('\n')
            

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

bot_commands.enable_commands(client)

if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()

    if PING_URL:
        threading.Thread(target=ping, args=(PING_URL,), daemon=True).start()
    else:
        print("PING_URL could not be found in .env")

    client.run(token=TOKEN)