import pandas as pd

class Backtester:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def run_backtest(self):
        # Assumes that data['signal'] is 1 or 0. 
        # Buy at close if signal=1, hold, else no position.
        # Compute strategy returns
        self.data['market_returns'] = self.data['close'].pct_change()
        self.data['strategy_returns'] = self.data['market_returns'] * self.data['signal'].shift(1)
        self.data['cumulative_returns'] = (1 + self.data['strategy_returns'].fillna(0)).cumprod()
        return self.data
