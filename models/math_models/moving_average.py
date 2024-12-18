import pandas as pd

def moving_average_strategy(data: pd.DataFrame, short_window=20, long_window=50):
    data = data.copy()
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()
    data['signal'] = 0
    data.loc[data['short_ma'] > data['long_ma'], 'signal'] = 1
    data = data.dropna().reset_index(drop=True)
    return data
