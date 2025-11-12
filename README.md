# Quote Bot
A discord bot that fetches quotes from [wisdomquotes.com](https://wisdomquotes.com/) using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and sends them in Discord channels. Supports slash commands.

# How It Works
1. When the first run, `bot.py` scrapes quotes from the selected sections of [wisdomquotes.com](https://wisdomquotes.com/) and saves them to a local JSON file.
2. Subsequent calls get quotes from the JSON file and only scrapes again if JSON is empty.
3. The bot interacts with discord using [Discord API](https://discord.com/developers/docs/).
