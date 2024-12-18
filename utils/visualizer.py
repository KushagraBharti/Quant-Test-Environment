import matplotlib.pyplot as plt

def plot_equity_curve(data):
    plt.figure(figsize=(12,6))
    plt.plot(data['timestamp'], data['cumulative_returns'], label='Strategy Equity Curve')
    plt.title('Strategy Performance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.tight_layout()
    plt.show()
