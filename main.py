import os
import logging
import time
from dotenv import load_dotenv
import pandas as pd

from utils.data_loader import DataLoader
from utils.feature_engineer import FeatureEngineer
from utils.backtester import Backtester
from utils.metrics import evaluate_performance
from utils.visualizer import plot_equity_curve
from utils.visualizer import plot_strategy_with_signals
from utils.trader_setup import get_paper_trading_client
from utils.paper_trader import PaperTrader
from utils.trade_logger import export_trade_log

# Strategy
from models.math_models.moving_average import moving_average_strategy

# Load environment variables
load_dotenv()

API_KEY = os.getenv("TRADE_API_KEY")
SECRET_KEY = os.getenv("TRADE_API_SECRET")
PAPER_API_BASE_URL = os.getenv("TRADE_API_URL")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def validate_env_vars():
    """Validate that all required environment variables are set."""
    if not all([API_KEY, SECRET_KEY, PAPER_API_BASE_URL]):
        raise EnvironmentError("Missing one or more required environment variables: TRADE_API_KEY, TRADE_API_SECRET, TRADE_API_URL.")

def main():
    # Validate environment variables
    validate_env_vars()
    
    symbol = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    # Step 1: Fetch Historical Data
    logger.info(f"Fetching historical data for {symbol} from {start_date} to {end_date}.")
    try:
        dl = DataLoader(API_KEY, SECRET_KEY)
        historical_data = dl.get_historical_data(symbol, start_date, end_date)
        if historical_data.empty:
            logger.error(f"No data fetched for {symbol}. Exiting.")
            return
        raw_path = os.path.join("data", "raw", f"{symbol}_{start_date}_{end_date}.csv")
        historical_data.to_csv(raw_path, index=False)
        logger.info(f"Historical data saved to {raw_path}.")
    except Exception as e:
        logger.exception(f"Error fetching historical data: {e}")
        return

    # Step 2: Preprocess & Feature Engineer
    logger.info("Preprocessing data and adding features.")
    try:
        fe = FeatureEngineer()
        processed_data = fe.add_features(historical_data)
        processed_path = os.path.join("data", "processed", f"{symbol}_{start_date}_{end_date}_processed.csv")
        processed_data.to_csv(processed_path, index=False)
        logger.info(f"Processed data saved to {processed_path}.")
    except Exception as e:
        logger.exception(f"Error in preprocessing or feature engineering: {e}")
        return

    # Step 3: Apply Strategy
    logger.info("Applying moving average strategy.")
    try:
        strategy_data = moving_average_strategy(processed_data, short_window=20, long_window=50)
    except Exception as e:
        logger.exception(f"Error applying strategy: {e}")
        return

    # Step 4: Backtest
    logger.info("Running backtest.")
    try:
        bt = Backtester(strategy_data)
        bt_results = bt.run_backtest()
        metrics = evaluate_performance(bt_results)
        logger.info(f"Backtest Metrics: {metrics}")
    except Exception as e:
        logger.exception(f"Error during backtest: {e}")
        return

    # Step 5: Visualize
    logger.info("Generating equity curve visualization.")
    try:
        #plot_equity_curve(bt_results)
        plot_strategy_with_signals(strategy_data)
    except Exception as e:
        logger.exception(f"Error during visualization: {e}")

    # Step 6: Output Results

    # Export trade log
    export_trade_log(strategy_data, model_name="moving_average_strategy")

    # Step 7: Paper Trade (optional)
    
    trading_client = get_paper_trading_client(API_KEY, SECRET_KEY, PAPER_API_BASE_URL)
    paper_trader = PaperTrader(trading_client)

    # Place Buy Order
    order = paper_trader.place_market_order(symbol, qty=1, side="buy")
    logger.info(f"Paper order placed: {order}")

    # Wait for the Buy Order to Be Filled
    while True:
        buy_order = trading_client.get_order_by_id(order.id)
        if buy_order.status == "filled":
            logger.info(f"Buy order filled at {buy_order.filled_avg_price}. Proceeding to sell.")
            break
        logger.info("Waiting for buy order to be filled...")
        time.sleep(2)  # Wait 2 seconds before checking again

    # Place Sell Order
    try:
        sell_order = paper_trader.place_market_order(symbol, qty=1, side="sell")
        logger.info(f"Paper order placed: {sell_order}")
    except Exception as e:
        logger.error(f"Error placing sell order for {symbol}: {e}")

if __name__ == "__main__":
    main()
