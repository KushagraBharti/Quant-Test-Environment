import pandas as pd

class FeatureEngineer:
    def __init__(self):
        pass

    def add_features(self, df: pd.DataFrame):
        if 'close' not in df:
            raise ValueError("DataFrame must contain 'close' column.")

        df = df.copy()
        df['return'] = df['close'].pct_change()

        # Example: Adding a moving average as a feature
        df['ma_20'] = df['close'].rolling(window=20).mean()
        df['ma_50'] = df['close'].rolling(window=50).mean()

        # Drop rows with NaN values created during calculations
        df = df.dropna().reset_index(drop=True)
        return df
