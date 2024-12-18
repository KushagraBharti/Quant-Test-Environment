import numpy as np
import pandas as pd

def evaluate_performance(data: pd.DataFrame):
    if 'strategy_returns' not in data or 'cumulative_returns' not in data:
        raise ValueError("Data must contain 'strategy_returns' and 'cumulative_returns' columns.")

    returns = data['strategy_returns'].dropna()
    if returns.empty or returns.std() == 0:
        return {"sharpe_ratio": None, "max_drawdown": None, "final_return": None}

    # Calculate Sharpe Ratio
    sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)

    # Calculate Max Drawdown
    cumulative = data['cumulative_returns']
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    metrics = {
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "final_return": cumulative.iloc[-1]
    }
    return metrics
