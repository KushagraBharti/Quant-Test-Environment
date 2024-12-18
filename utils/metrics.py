import numpy as np
import pandas as pd

def evaluate_performance(data: pd.DataFrame):
    returns = data['strategy_returns'].dropna()
    if returns.empty or returns.std() == 0:
        return {"sharpe_ratio": None, "max_drawdown": None, "final_return": data['cumulative_returns'].iloc[-1]}

    # Assuming daily returns
    sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
    
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
