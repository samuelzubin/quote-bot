import requests
from bs4 import BeautifulSoup
import random
import json

#Website URL
main_url: str = "https://libquotes.com/"

#Quote keywords
subsection = ['change-quotes', 'pain-quotes', 'thought-quotes', 'time-quotes', 'learn-quotes']

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
            page_number: int = 1

            #Find number of pages per author
            url: str = main_url + section
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            page_footer = soup.find("ul", class_="pager nomargin")

            if page_footer:
                pages: list = page_footer.find_all("li")
                last_page: int = int(pages[-1].text.strip())
            else:
                last_page = 1
            
            #Get all quotes on all pages
            while True:
                url: str = main_url + section + "/" + str(page_number)
                page: requests.Response = requests.get(url)
                soup = BeautifulSoup(page.content, "html.parser")

                #Get quotes and authors
                quote_divs: list = soup.find_all("div", class_="panel-body")
                for div in quote_divs:
                    quote: str = div.find("span", class_="quote_span").text.strip()
                    try:
                        author: str = div.find("span", class_="fda").text.strip()
                    except:
                        author: str = div.find_all("a")[-1].text.strip()
                                        
                    #Append to list if quote doesn't exceed character limit
                    if len(quote) <= 100:
                        data.append([quote, author])

                #Check if there are more pages
                next_page = True if page_number < last_page else False    

                #Go to next page if there is one
                page_number += 1

                if not next_page:
                    break
        
        #Write to json
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return data if data else []
    
def get_random_quote(quote_list) -> str:    
    random_value = random.randint(0, len(quote_list))
    return (f"*{quote_list[random_value][0]}*")