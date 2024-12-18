import pandas as pd
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data import DataFeed

class DataLoader:
    def __init__(self, api_key, secret_key):
        self.client = StockHistoricalDataClient(api_key, secret_key)

    def get_historical_data(self, symbol: str, start: str, end: str, timeframe=TimeFrame.Day):
        """
        Fetch historical OHLCV data for a given symbol from Alpaca.

        Parameters:
        - symbol (str): The stock ticker symbol (e.g., "AAPL").
        - start (str): Start date in ISO 8601 format (e.g., "2022-01-01").
        - end (str): End date in ISO 8601 format (e.g., "2023-01-01").
        - timeframe (TimeFrame): Granularity of the bars (default: TimeFrame.Day).

        Returns:
        - pd.DataFrame: DataFrame with historical OHLCV data.
        """
        # Validate inputs
        if not symbol or not start or not end:
            raise ValueError("Symbol, start, and end dates are required.")
        
        # Create request parameters
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=timeframe,
            start=start,
            end=end,
            feed=DataFeed.IEX  # Use IEX for free data
        )

        try:
            # Fetch bar data
            bars = self.client.get_stock_bars(request_params)
            
            # Convert to a DataFrame
            df = bars.df  # Updated to use the `.df` property
            
            # Ensure the symbol exists in the returned data
            if symbol not in df.index.levels[0]:
                raise ValueError(f"No data found for {symbol} in the specified date range.")
            
            # Filter and reset index
            df = df.loc[symbol].reset_index()

            # Rename columns for consistency
            df = df.rename(columns={'timestamp': 'timestamp'})
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            return df

        except Exception as e:
            raise RuntimeError(f"Error fetching historical data: {e}")
