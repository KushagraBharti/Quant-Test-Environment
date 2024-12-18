import os
from dotenv import load_dotenv
import pandas as pd

from utils.data_loader import DataLoader
from utils.feature_engineer import FeatureEngineer
from utils.backtester import Backtester
from utils.metrics import evaluate_performance
from utils.visualizer import plot_equity_curve
from utils.trader_setup import get_paper_trading_client
from utils.paper_trader import PaperTrader

# Strategy
from models.math_models.moving_average import moving_average_strategy

load_dotenv()

API_KEY = os.getenv("TRADE_API_KEY")
SECRET_KEY = os.getenv("TRADE_API_SECRET")
PAPER_API_BASE_URL = os.getenv("TRADE_API_URL")

def main():
    symbol = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    # 1. Fetch Historical Data
    dl = DataLoader(API_KEY, SECRET_KEY)
    historical_data = dl.get_historical_data(symbol, start_date, end_date)
    raw_path = os.path.join("data", "raw", f"{symbol}_{start_date}_{end_date}.csv")
    historical_data.to_csv(raw_path, index=False)

    # 2. Preprocess & Feature Engineer
    fe = FeatureEngineer()
    processed_data = fe.add_features(historical_data)
    processed_path = os.path.join("data", "processed", f"{symbol}_{start_date}_{end_date}_processed.csv")
    processed_data.to_csv(processed_path, index=False)

    # 3. Apply Strategy
    strategy_data = moving_average_strategy(processed_data, short_window=20, long_window=50)

    # 4. Backtest
    bt = Backtester(strategy_data)
    bt_results = bt.run_backtest()
    metrics = evaluate_performance(bt_results)
    print("Backtest Metrics:", metrics)

    # 5. Visualize
    plot_equity_curve(bt_results)

    # 6. Paper Trade (optional)
    # Only proceed if you want to test placing a mock order in paper environment
    # This code snippet simply places a sample market order if last signal is '1'.
    trading_client = get_paper_trading_client(API_KEY, SECRET_KEY, PAPER_API_BASE_URL)
    paper_trader = PaperTrader(trading_client)
    last_signal = strategy_data['signal'].iloc[-1]
    if last_signal == 1:
        # Example: Buy 1 share of AAPL
        order = paper_trader.place_market_order(symbol, qty=1, side="buy")
        print("Paper order placed:", order)

if __name__ == "__main__":
    main()
