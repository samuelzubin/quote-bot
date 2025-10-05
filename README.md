# Quote Bot
A discord bot that fetches quotes from [libquotes.com](https://libquotes.com/) using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and periodically (or through commands) sends them in Discord channels

# How It Works
1. When the first run, `bot.py` scrapes quotes from the selected sections of [libquotes.com](https://libquotes.com/) and saves them to a local JSON file
2. Subsequent runs read quotes from the JSON file instead of scraping again
3. The bot interacts with discord using [Discord API](https://discord.com/developers/docs/).
