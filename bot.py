import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from responses import get_response
import bot_commands

#LOAD ENVIRONMENT VARIABLES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = discord.Object(id=int(os.getenv('GUILD_ID')))


class Client(commands.Bot):
    async def on_ready(self):
        #SYNC COMMANDS
        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f"Synced {len(synced)} command(s) to guild {GUILD_ID}")
        except Exception as e:
            print(f"Error syncing commands: {e}")


        print(f"{self.user.display_name} is online!")

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if 'jaq' in message.content.lower():
            await message.channel.send(get_response())

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

bot_commands.enable_commands(client)


client.run(token=TOKEN)