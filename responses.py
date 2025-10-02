from quotes import get_random_quote, fetch_quote

quotes = []

def get_response(user_input: str) -> str:
    global quotes
    if 'jaq' in user_input.lower() or 'quote':
        if not quotes:
            quotes = fetch_quote()
        return get_random_quote(quotes, user_input)