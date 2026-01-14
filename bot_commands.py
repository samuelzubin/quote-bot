import asyncio
import discord
from datetime import datetime
from discord import app_commands
from responses import get_response
from scheduling import QuoteScheduler


auto_quote_tasks = {}
scheduled_quote_tasks = {}

#SLASH COMMANDS
def enable_commands(client):
    # /help
    @client.tree.command(name="help", description="Information about Jaquavius bot")
    async def help(interaction: discord.Interaction):
        help_embed = discord.Embed(
            title="I am Jaquavius, provider of quotes!",
            description="*I provide inspiration and enlightenment. Don't call me, I'll call you. I don't need to be asked to start sending quotes. I'll send you one every day (unless you request otherwise). Oh, and if I hear my name, I won't hesitate to chime in.*\n\n__**Commands**__\n\nQuote: Sends a quote\n\nAuto-quote: Allows you to enable/disable automatic quotes and set the interval (minutes)",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=help_embed, ephemeral=True)

    # /quote
    @client.tree.command(name="quote", description="Send a quote")
    async def send_quote(interaction: discord.Interaction):
        try:
            await interaction.response.send_message(get_response())
        except discord.errors.NotFound:
            print("Please wait while data.json populates with quotes")

    # /auto-quote
    @client.tree.command(name="auto-quote", description="Send a quote periodically")
    @app_commands.describe(
        toggle_on_off="Enable or disable auto-quote",
        interval="Specify quote interval in minutes (Default: 1 day)"
    )
    async def auto_quote(interaction: discord.Interaction, toggle_on_off: bool = True, interval: int = 60 * 24):
        channel = interaction.channel
        if toggle_on_off:
            if channel.id in auto_quote_tasks:
                auto_quote_tasks[channel.id].cancel()
            
            if interval > 0:
                task = asyncio.create_task(send_quotes(channel, interval))
                auto_quote_tasks[channel.id] = task
                if interval == 1:
                    await interaction.response.send_message(f"✅ _Auto-quote enabled every minute_")
                elif interval == 60:
                    await interaction.response.send_message(f"✅ _Auto-quote enabled every hour_")
                elif interval >= 60:
                    if interval % 60 == 0:
                        await interaction.response.send_message(f"✅ _Auto-quote enabled every {interval/60:.0f} hours_")
                    else:
                        await interaction.response.send_message(f"✅ _Auto-quote enabled every {interval/60:.1f} hours_")
                else:
                    await interaction.response.send_message(f"✅ _Auto-quote enabled every {interval} minutes_")
            else:
                await interaction.response.send_message("Please enter a postive integer!", ephemeral=True)
        else:
            if channel.id in auto_quote_tasks:
                auto_quote_tasks[channel.id].cancel()
                del auto_quote_tasks[channel.id]
                await interaction.response.send_message(f"🛑 _Auto-quote disabled_")
            else:
                await interaction.response.send_message("_Auto-quote is already disabled_", ephemeral=True)
                
    @client.tree.command(name="schedule", description="Allows you to schedule quotes at specific dates and times")
    @app_commands.describe(
        schedule="Specify date and time (in PT) to schedule quote (Format: MM-DD-YY HH:MM)",
        interval="Specify interval for quote to reoccur in days (Default: 1 day) (Type 0 for one-time only)",
        enable="Enable (True) or disable (False) scheduled quotes"
    )
    async def schedule_quote(interaction: discord.Interaction, schedule: str, interval: int = 1, enable: bool = True):
        channel = interaction.channel
        if enable:
            if channel.id in scheduled_quote_tasks:
                scheduled_quote_tasks[channel.id].cancel()
                
            scheduler = QuoteScheduler(interval)
            if not scheduler.is_valid_interval():
                await interaction.response.send_message("Interval must be 0 or greater!", ephemeral=True)
                return
            if not scheduler.is_valid_schedule(schedule):
                await interaction.response.send_message("Invalid date/time format! Please use MM-DD-YY HH:MM or MM-DD HH:MM (Military Time)", ephemeral=True)
                return
            
            
            delay = scheduler.calculate_delay(datetime.now()) # schedule date - current date in seconds
            if delay < 0:
                await interaction.response.send_message("Scheduled time must be in the future!", ephemeral=True)
                return
            task = asyncio.create_task(send_scheduled_quotes(channel, delay, interval))
            scheduled_quote_tasks[channel.id] = task
            await interaction.response.send_message(f"✅ _Scheduled quotes enabled starting {scheduler.to_string()} every {interval} day(s)_")
            
        else:
            if channel.id in scheduled_quote_tasks:
                scheduled_quote_tasks[channel.id].cancel()
                del scheduled_quote_tasks[channel.id]
                await interaction.response.send_message(f"🛑 _Scheduled quotes disabled_")
            else:
                await interaction.response.send_message("_Scheduled quotes are already disabled_", ephemeral=True)
    

async def send_quotes(channel, interval):
    try:
        while True:
            await asyncio.sleep(interval * 60)  #Convert to minutes
            await channel.send(get_response())
    except asyncio.CancelledError:
        pass 

async def send_scheduled_quotes(channel, delay, interval):
    try:
        await asyncio.sleep(delay)
        await channel.send(get_response())
        send_quotes(channel, interval)
    except asyncio.CancelledError:
        return