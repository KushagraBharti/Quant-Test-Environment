import matplotlib.pyplot as plt

def plot_equity_curve(data):
    if 'timestamp' not in data or 'cumulative_returns' not in data:
        raise ValueError("Data must contain 'timestamp' and 'cumulative_returns' columns.")

    plt.figure(figsize=(12, 6))
    plt.plot(data['timestamp'], data['cumulative_returns'], label='Strategy Equity Curve', color='blue')
    plt.title('Strategy Performance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.show()

def plot_strategy_with_signals(data):
    """
    Visualizes the stock prices, moving averages, and buy/sell signals.

    Parameters:
    - data (pd.DataFrame): Processed DataFrame with 'close', 'short_ma', 'long_ma', and 'signal' columns.
    """
    if not all(col in data.columns for col in ['close', 'short_ma', 'long_ma', 'signal']):
        raise ValueError("Data must contain 'close', 'short_ma', 'long_ma', and 'signal' columns.")

    # Create the plot
    plt.figure(figsize=(14, 7))
    
    # Plot the closing prices and moving averages
    plt.plot(data['timestamp'], data['close'], label='Close Price', linewidth=1.5, alpha=0.8)
    plt.plot(data['timestamp'], data['short_ma'], label='Short Moving Average (20)', linewidth=1)
    plt.plot(data['timestamp'], data['long_ma'], label='Long Moving Average (50)', linewidth=1)
    
    # Mark buy (signal == 1) and sell (signal == -1) points
    buy_signals = data[data['signal'] == 1]
    sell_signals = data[data['signal'] == -1]

    plt.scatter(buy_signals['timestamp'], buy_signals['close'], label='Buy Signal', color='green', marker='o', alpha=0.9)
    plt.scatter(sell_signals['timestamp'], sell_signals['close'], label='Sell Signal', color='red', marker='o', alpha=0.9)

    # Add titles and labels
    plt.title('Trading Strategy with Buy/Sell Signals', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # Show the plot
    plt.show()
