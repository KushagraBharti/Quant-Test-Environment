import pandas as pd

class FeatureEngineer:
    def __init__(self):
        pass

    def add_features(self, df: pd.DataFrame):
        df = df.copy()
        df['return'] = df['close'].pct_change()
        # More features can be added. For now, just returns. 
        # Strategy code will add MAs itself, but you can also do them here.
        df = df.dropna().reset_index(drop=True)
        return df
