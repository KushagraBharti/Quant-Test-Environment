from alpaca.trading.client import TradingClient

def get_paper_trading_client(api_key, secret_key, base_url):
    # paper=True sets the domain to paper-api.alpaca.markets by default, but we can override URL if needed.
    client = TradingClient(api_key=api_key, secret_key=secret_key, paper=True)
    return client
