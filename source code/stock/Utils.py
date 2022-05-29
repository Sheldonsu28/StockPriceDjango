import yfinance as yf


def verify_symbol(symbol: str) -> bool:
    """
    Query the symbol with yahoo server
    """
    stock = yf.Ticker(symbol)
    return 'symbol' in stock.info


def batch_get_symbol_price(symbols: list) -> list:
    """
    Query the symbol with yahoo server
    """
    query = "".join([' ' + s for s in symbols])
    response = yf.Tickers(query.strip()).tickers

    return [{'ticker': ticker, 'price': response[ticker].info['regularMarketPrice']} for ticker in response.keys()]
