import requests
from bs4 import BeautifulSoup
import random

#Website URL
main_url: str = "https://quotes.toscrape.com/"


def fetch_quote() -> list:
    data = []
    url: str = main_url
    page_number: int = 1

    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        #Get quotes and authors
        quote_divs: list = soup.find_all("div", class_="quote")
        for div in quote_divs:
            quote: str = div.find("span", class_="text").text.strip()
            author: str = div.find("small", class_="author").text.strip()
            
            #Append to list
            data.append([quote, author])

            # print(f"{quote} by {author}")

        #Check if there are more pages, break if not
        next_page = True if (soup.find("li", class_="next") != None) else False
        
        #Go to next page if there is one
        page_number += 1
        url = main_url + "page/" + str(page_number)

        if not next_page:
            break

    return data if data else []
    

def get_random_quote(quote_list, user_input) -> str:    
    random_value = random.randint(0, len(quote_list))
    
    return (f"*{quote_list[random_value][0]}*\n-Jaquavius")