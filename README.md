# Quant-Test-Environment
Testing Environment to test Quant strategies (Math, ML, and Sentiment Analysis models)

Testing...

project/

├── data/

│   ├── raw/                # Raw, unprocessed data (2000–2023 and 2024–present)

│   ├── processed/          # Preprocessed data, ready for modeling

├── models/

│   ├── math_models/        # Mathematical models (e.g., moving averages, mean reversion)

│   ├── ml_models/          # Machine learning models (e.g., regression, classifiers)

│   ├── sentiment_models/   # Sentiment analysis models (e.g., NLP-based)

├── utils/

│   ├── data_loader.py      # Unified data loader for raw and processed data

│   ├── feature_engineer.py # Scripts for generating technical indicators, derived features

│   ├── backtester.py       # Unified backtesting framework

│   ├── visualizer.py       # Visualization tools for interactive graphs

├── main.py                 # Central script to coordinate testing and results
