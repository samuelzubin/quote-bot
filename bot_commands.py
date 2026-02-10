import asyncio
import discord
from datetime import datetime
from zoneinfo import ZoneInfo
from discord import app_commands
from responses import get_response
from scheduling import QuoteScheduler

TIMEZONE = ZoneInfo('America/Los_Angeles')

auto_quote_tasks = {}
scheduled_quote_tasks: dict = {} # Key: channel id | Value: list of tasks
months_choices = [
    app_commands.Choice(name="January", value='01'), app_commands.Choice(name="February", value='02'), app_commands.Choice(name="March", value='03'), 
    app_commands.Choice(name="April", value='04'), app_commands.Choice(name="May", value='05'), app_commands.Choice(name="June", value='06'),
    app_commands.Choice(name="July", value='07'), app_commands.Choice(name="August", value='08'), app_commands.Choice(name="September", value='09'), 
    app_commands.Choice(name="October", value='10'), app_commands.Choice(name="November", value='11'), app_commands.Choice(name="December", value='12')
]
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
        month="Select month from dropdown",
        day="Type day as a number (No Leading Zeros)",
        time="Type time in HH:MM (Military Time) format",
        interval="Specify interval for quote to reoccur in days (Default: 1 day) (Type 0 for one-time only)",
    )
    @app_commands.choices(month=months_choices)
    async def schedule_quote(interaction: discord.Interaction, month: app_commands.Choice[str], day: int, time: str, interval: int = 1):
        # await interaction.response.send_message(f"parameters: {dates}, {interval}, {is_enable}", ephemeral=True)
        # First parse the string and add to a list of datetime objects
        
        # If one of the time is invalid, return an error message
        channel = interaction.channel
        
        formatted_date = f"{month.value}-{day}-{datetime.now(tz=TIMEZONE).year} {time}" 

        scheduler = QuoteScheduler(interval, TIMEZONE)
        if not scheduler.is_valid_interval():
            await interaction.response.send_message("Interval must be 0 or greater!", ephemeral=True)
            return
        if not scheduler.is_valid_schedule(formatted_date):
            await interaction.response.send_message("Invalid date/time format! Please use HH:MM (Military Time)", ephemeral=True)
            return
        
        
        delay = scheduler.calculate_delay(datetime.now(tz=TIMEZONE)) # schedule date - current date in seconds
        task = asyncio.create_task(send_scheduled_quotes(channel, delay, interval))
        if channel.id not in scheduled_quote_tasks:
            scheduled_quote_tasks[channel.id] = []
        
        if interval == 0:
            response = f"_Scheduled one-time quote for {scheduler.to_string()}_"
        else:
            response = f"_Scheduled quotes starting {scheduler.to_string()} every {interval} day(s)_"
        scheduled_quote_tasks[channel.id].append((task, response))
        await interaction.response.send_message(response)
            
                
    @client.tree.command(name="list_schedule", description="Check your scheduled quotes")
    async def schedule_list(interaction: discord.Interaction):
        channel = interaction.channel
        if channel.id in scheduled_quote_tasks and scheduled_quote_tasks[channel.id]:
            response = "📅 __**Scheduled Quotes:**__\n"
            for i, (task, desc) in enumerate(scheduled_quote_tasks[channel.id], start=1):
                response += f"{i}. {desc}\n"
            await interaction.response.send_message(response)
        else:
            await interaction.response.send_message("_No scheduled quotes for this channel_", ephemeral=True)
            
    @client.tree.command(name="delete_schedule", description="Delete the last scheduled quote")
    async def schedule_delete(interaction: discord.Interaction):
        channel = interaction.channel
        if channel.id not in scheduled_quote_tasks or not scheduled_quote_tasks[channel.id]:
            await interaction.response.send_message("_Scheduled quotes are already disabled for this channel_", ephemeral=True)
        else:
            recent_task = scheduled_quote_tasks[channel.id].pop()
            recent_task[0].cancel()
            await interaction.response.send_message(f"🛑 Disabled {recent_task[1]}")
    

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
        if interval > 0: # If interval is 0, do not reschedule
            await send_quotes(channel, interval*24*60) # convert days to hours
    except asyncio.CancelledError:
        pass