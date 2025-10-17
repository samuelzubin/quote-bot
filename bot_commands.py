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
        help_embed = discord.Embed(
            title="I am Jaquavius, provider of quotes!",
            description="*I send a quote when I hear my name. I can also send quotes periodically.*\n\n\n**Commands**\n\nQuote: Sends a quote\n\nAuto-quote: Allows you to enable/disable automatic quotes and set the interval (minutes)",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=help_embed, ephemeral=True)

    # /quote
    @client.tree.command(name="quote", description="Send a random quote")
    async def send_quote(interaction: discord.Interaction):
        try:
            await interaction.response.send_message(get_response())
        except discord.errors.NotFound:
            print("Please wait while data.json populates with quotes")

    # /auto-quote
    @client.tree.command(name="auto-quote", description="Sends a quote periodically")
    @app_commands.describe(
        toggle_on_off="Enable or disable auto-quote",
        interval="Specify quote interval in minutes (Default: 1 day)"
    )
    async def auto_quote(interaction: discord.Interaction, toggle_on_off: bool = True, interval: int = 60 * 24):
        channel = interaction.channel
        if toggle_on_off:
            if channel.id in quote_tasks:
                quote_tasks[channel.id].cancel()
            
            if interval > 0:
                task = asyncio.create_task(send_quotes(channel, interval))
                quote_tasks[channel.id] = task
                if interval == 1:
                    await interaction.response.send_message(f"✅ _Auto-quote enabled every minute_")
                else:
                    await interaction.response.send_message(f"✅ _Auto-quote enabled every {interval} minutes_")
            else:
                await interaction.response.send_message("Please enter a postive integer!", ephemeral=True)
        else:
            if channel.id in quote_tasks:
                quote_tasks[channel.id].cancel()
                del quote_tasks[channel.id]
                await interaction.response.send_message(f"🛑 _Auto-quote disabled_")
            else:
                await interaction.response.send_message("Auto-quote is not running in this channel")


async def send_quotes(channel, interval):
    try:
        while True:
            await asyncio.sleep(interval * 60)  #Convert to minutes
            await channel.send(get_response())
    except asyncio.CancelledError:
        pass 