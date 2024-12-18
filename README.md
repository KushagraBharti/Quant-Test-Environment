# Quant-Test-Environment
Testing Environment to test Quant strategies (Math, ML, and Sentiment Analysis models)

This project provides a modular framework to:
- Fetch and preprocess historical data from Alpaca.
- Apply various trading strategies (mathematical, ML-based, sentiment-based).
- Backtest strategies on historical data.
- Visualize results and performance metrics.
- Paper trade promising strategies on Alpaca.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Setup .env file:
   ```env
   TRADE_API_KEY="your_alpaca_key"
   TRADE_API_SECRET="your_alpaca_secret_key"
   TRADE_API_URL="alpaca_provided_url"

3. Should be able to run everything as is.

## Project Structure

```
project/
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   ├── math_models/
│   │   └── moving_average.py
│   ├── ml_models/
│   │   └── example_ml_model.py
│   ├── sentiment_models/
│       └── sentiment_example.py
├── utils/
│   ├── data_loader.py
│   ├── feature_engineer.py
│   ├── backtester.py
│   ├── metrics.py
│   ├── paper_trader.py
│   ├── visualizer.py
│   └── trader_setup.py
├── logs/
│   └── run.log
├── main.py
├── .env
├── requirements.txt
└── README.md
```