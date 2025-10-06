import asyncio
import discord
from discord import app_commands
from responses import get_response

quote_tasks = {}

#SLASH COMMANDS
def enable_commands(client):
    # /help
    @client.tree.command(name="help", description="Get info about Jaquavius bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.send_message("*I am Jaquavius, provider of quotes!*\n\nI send a quote when I hear my name. By default, I'll also send a quote every 24hrs.\n\n__*Commands*__\n\nquote: Sends a quote\nauto-quote: Allows you to enable/disable automatic quotes and set the interval (minutes)", ephemeral=True)

    # /quote
    @client.tree.command(name="quote", description="Send a random quote")
    async def send_quote(interaction: discord.Interaction):
        await interaction.response.send_message(get_response())

    # /auto-quote
    @client.tree.command(name="auto-quote", description="Sends a quote periodically")
    @app_commands.describe(
        enable="Enable or disable auto-quote",
        interval="Specify quote interval in minutes (Default: 1 day)"
    )
    async def auto_quote(interaction: discord.Interaction, enable: bool = True, interval: int = 60 * 24):
        channel = interaction.channel
        if enable:
            if channel.id in quote_tasks:
                quote_tasks[channel.id].cancel()
            
            task = asyncio.create_task(send_quotes(channel, interval))
            quote_tasks[channel.id] = task
            await interaction.response.send_message(f"✅ _Auto-quote enabled every {interval} minutes_")
        else:
            if channel.id in quote_tasks:
                quote_tasks[channel.id].cancel()
                del quote_tasks[channel.id]
                await interaction.response.send_message(f"🛑 _Auto-quote disabled_")
            else:
                await interaction.response.send_message("Auto-quote is not running in this channel.")


async def send_quotes(channel, interval):
    try:
        while True:
            await asyncio.sleep(interval * 60)  #Convert to minutes
            await channel.send(get_response())
    except asyncio.CancelledError:
        pass 