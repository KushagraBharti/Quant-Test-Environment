import pandas as pd
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data import DataFeed

class DataLoader:
    def __init__(self, api_key, secret_key):
        self.client = StockHistoricalDataClient(api_key, secret_key)

    def get_historical_data(self, symbol: str, start: str, end: str):
        # Fetch daily bars
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,  # single symbol as a string
            timeframe=TimeFrame.Day,
            start=start,
            end=end,
            feed=DataFeed.IEX  # Use IEX feed for free data
        )

        # This will return a Bars object (not MultiBars)
        bars = self.client.get_stock_bars(request_params)

        # Convert directly to a DataFrame
        df = bars.to_df().reset_index()

        # Rename and select relevant columns
        df = df.rename(columns={'timestamp': 'timestamp'})
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        df = df.sort_values('timestamp').reset_index(drop=True)
        return df
