from quotes import get_random_quote, fetch_quote

quotes = []

def get_response() -> str:
    global quotes
    if not quotes:
        quotes = fetch_quote()
    return get_random_quote(quotes) + "\n-Jaquavius"