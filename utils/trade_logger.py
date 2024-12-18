import pandas as pd
import os

def export_trade_log(strategy_data: pd.DataFrame, model_name: str, output_folder: str = "models/math_models/outputs"):
    """
    Exports a trade log detailing buy/sell movements and profits.

    Parameters:
    - strategy_data (pd.DataFrame): DataFrame with 'timestamp', 'close', and 'signal'.
    - model_name (str): Name of the model used (e.g., "moving_average_strategy").
    - output_folder (str): Folder to save the trade log file.
    """
    if not all(col in strategy_data.columns for col in ['timestamp', 'close', 'signal']):
        raise ValueError("Data must contain 'timestamp', 'close', and 'signal' columns.")
    
    trades = []
    position = 0
    total_profit = 0
    last_buy_price = None

    for i, row in strategy_data.iterrows():
        if row['signal'] == 1:  # Buy signal
            position += 1
            last_buy_price = row['close']
            trades.append({
                "Date": row['timestamp'],
                "Type": "Buy",
                "Price": row['close'],
                "Quantity": 1,
                "Profit/Loss": None
            })
        elif row['signal'] == -1 and position > 0:  # Sell signal
            profit = row['close'] - last_buy_price
            total_profit += profit
            trades.append({
                "Date": row['timestamp'],
                "Type": "Sell",
                "Price": row['close'],
                "Quantity": 1,
                "Profit/Loss": profit
            })
            position -= 1

    # Add summary row for total profit
    trades.append({
        "Date": "Total",
        "Type": "",
        "Price": "",
        "Quantity": "",
        "Profit/Loss": total_profit
    })

    # Convert to DataFrame
    trades_df = pd.DataFrame(trades)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Generate filename dynamically
    filename = os.path.join(output_folder, f"{model_name}_trade_log.csv")

    # Save to CSV
    trades_df.to_csv(filename, index=False)

    print(f"Trade log saved to {filename}")
