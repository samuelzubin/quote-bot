import requests
from bs4 import BeautifulSoup

def main() -> None:
    URL = "https://quotes.toscrape.com/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    quote_container: list = soup.find_all("div", class_="col-md-8")
    quote_container.pop(0)
    for div in quote_container:                               #Iterate through the one item in quote_container
        quotes: list = div.find_all("span", class_="text")    #Get all span elements on the page
        for quote in quotes:                                  #Iterate through all span elements
            print(quote.text.strip())
            print("\n")

if __name__ == "__main__":
    main()