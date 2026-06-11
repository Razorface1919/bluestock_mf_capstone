import pandas as pd
import numpy as np
from pathlib import Path

def compute_performance_metrics():
    print("Calculating system-wide performance and risk metrics...")
    
    # 1. Dynamic Path Resolution
    BASE_DIR = Path(__file__).resolve().parent.parent 
    PROCESSED_DIR = BASE_DIR / "data" / "processed"
    
    nav_df = pd.read_csv(PROCESSED_DIR / "clean_nav.csv")
    perf_df = pd.read_csv(PROCESSED_DIR / "clean_performance.csv")

    # Sorting and establish daily returns
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.sort_values(['amfi_code', 'date'])
    nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()

    metrics = []
    rf_rate = 0.065 # 6.5% RBI repo rate proxy from project handbook

    for amfi, group in nav_df.groupby('amfi_code'):
        returns = group['daily_return'].dropna()
        n_trading_days = len(returns)
        
        if n_trading_days < 20:
            continue

        # 2. Correcting Geometric CAGR & Volatility
        nav_start = group['nav'].iloc[0]
        nav_end = group['nav'].iloc[-1]
        
        # Annualizing using actual trading days observed
        ann_return = ((nav_end / nav_start) ** (252 / n_trading_days)) - 1 
        ann_volatility = returns.std() * np.sqrt(252)

        # 3. Sharpe Ratio
        sharpe = (ann_return - rf_rate) / ann_volatility if ann_volatility > 0 else 0

        # 4. Maximum Drawdown Calculation
        nav_series = group['nav'].values
        running_max = np.maximum.accumulate(nav_series)
        drawdowns = (nav_series - running_max) / running_max
        max_dd = drawdowns.min()

        metrics.append({
            'amfi_code': amfi,
            'Calculated_Ann_Return': ann_return,
            'Calculated_Volatility': ann_volatility,
            'Calculated_Sharpe': sharpe,
            'Calculated_Max_Drawdown': max_dd
        })

    metrics_df = pd.DataFrame(metrics)
    
    output_path = PROCESSED_DIR / "calculated_performance_metrics.csv"
    metrics_df.to_csv(output_path, index=False)
    
    print(f"Metrics calculated and exported to {output_path}")
    return metrics_df

if __name__ == "__main__":
    compute_performance_metrics()