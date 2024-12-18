from alpaca.trading.client import TradingClient

def get_paper_trading_client(api_key, secret_key, base_url=None):
    if not api_key or not secret_key:
        raise ValueError("API key and secret key are required.")
    
    try:
        client = TradingClient(api_key=api_key, secret_key=secret_key, paper=True)
    except Exception as e:
        raise RuntimeError(f"Error initializing trading client: {e}")
    
    return client
