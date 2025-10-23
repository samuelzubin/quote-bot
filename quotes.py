import requests
from bs4 import BeautifulSoup
import random
import json
import re

#Website URL
main_url: str = 'https://wisdomquotes.com/'

#Quote keywords
subsection = ['never-give-up-quotes', 'understanding-quotes', 'strength-quotes', 'words-of-wisdom',
              'respect-quotes', 'responsibility-quotes', 'serenity-quotes']

def fetch_quote() -> list:
    data = []

    #Load from json or create new one
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    
    if data == []:
        for section in subsection:
            url: str = main_url + section
            page: requests.Response = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            
            #Get all quotes on all pages
            quote_blocks: list = soup.find_all("blockquote")
            for quote_block in quote_blocks:
                quote: str = quote_block.find("p").text.strip()
                                    
                #Append to list if quote doesn't exceed character limit
                if len(quote) <= 100:
                    pattern = r"^(.*?[\.!?])\s+([A-Z][A-Za-z\.\'\-éèáàïü\s]+)$"
                    match: re.Match = re.match(pattern, quote.strip())
                    try:
                        data.append([match.group(1), match.group(2)])
                    except:
                        pass
        
        #Write to json
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return data if data else []
    
def get_random_quote(quote_list) -> str:    
    random_value = random.randint(0, len(quote_list) - 1)
    return (f"*{quote_list[random_value][0]}*")