import requests
from bs4 import BeautifulSoup
import random

#Website URLs
author_pages = ['aristotle', 'marcus-aurelius', 'charles-darwin', 'hank-aaron', 'rené-descartes']
main_url: str = "https://libquotes.com/"

def fetch_quote() -> list:
    data = []
    for current_author in author_pages:
        page_number: int = 1

        while True:
            url: str = main_url + current_author
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            #Get quotes and authors
            quote_divs: list = soup.find_all("div", class_="panel-body")
            for div in quote_divs:
                quote: str = div.find("span", class_="quote_span").text.strip()
                author: str = div.find("span", class_="fda").text.strip()
                
                #Append to list
                data.append([quote, author])

            #Check if there are more pages, break if not
            if current_author == 'aristotle':
                next_page = True if page_number < 20 else False
            elif current_author == 'marcus-aurelius':
                next_page = True if page_number < 18 else False
            else:
                next_page = True if page_number < 13 else False
                

            #Go to next page if there is one
            page_number += 1
            url = main_url + str(page_number)

            if not next_page:
                break

    return data if data else []
    
def get_random_quote(quote_list) -> str:    
    random_value = random.randint(0, len(quote_list))
    return (f"*{quote_list[random_value][0]}*\n-{quote_list[random_value][1]}")