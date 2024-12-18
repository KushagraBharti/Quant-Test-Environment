import pandas as pd

def moving_average_strategy(data: pd.DataFrame, short_window=20, long_window=50):
    """
    Implements a moving average crossover strategy.
    
    Parameters:
    - data (pd.DataFrame): Input DataFrame containing at least a 'close' column.
    - short_window (int): Lookback period for the short moving average.
    - long_window (int): Lookback period for the long moving average.

    Returns:
    - pd.DataFrame: DataFrame with added columns for moving averages and trading signals.
    """
    # Input validation
    if 'close' not in data:
        raise ValueError("Input data must contain a 'close' column.")
    if not isinstance(short_window, int) or not isinstance(long_window, int):
        raise TypeError("Window sizes must be integers.")
    if short_window <= 0 or long_window <= 0:
        raise ValueError("Window sizes must be positive integers.")
    if short_window >= long_window:
        raise ValueError("Short window size must be less than the long window size.")

    # Copy data to avoid modifying the original DataFrame
    data = data.copy()

    # Calculate moving averages
    data['short_ma'] = data['close'].rolling(window=short_window, min_periods=1).mean()
    data['long_ma'] = data['close'].rolling(window=long_window, min_periods=1).mean()

    # Generate trading signals
    data['signal'] = 0
    data.loc[(data['short_ma'] > data['long_ma']) & (data['short_ma'].shift(1) <= data['long_ma'].shift(1)), 'signal'] = 1  # Buy signal
    data.loc[(data['short_ma'] < data['long_ma']) & (data['short_ma'].shift(1) >= data['long_ma'].shift(1)), 'signal'] = -1  # Sell signal

    # Drop rows with NaN values caused by rolling window
    data = data.dropna().reset_index(drop=True)

    return data
