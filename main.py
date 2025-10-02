import requests
from bs4 import BeautifulSoup

#Website URL
main_url: str = "https://quotes.toscrape.com/"

data = {}

def main() -> None:
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
            
            #Append to dictionary
            data.update({quote: author})

            # print(f"{quote} by {author}")

        #Check if there are more pages, break if not
        next_page = True if (soup.find("li", class_="next") != None) else False
        if not next_page:
            break

        #Go to next page if there is one
        page_number += 1
        url = main_url + "page/" + str(page_number)

if __name__ == "__main__":
    main()