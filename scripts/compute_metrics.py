import pandas as pd
import numpy as np

def compute_performance_metrics():
    print("Calculating system-wide performance and risk metrics...")
    nav_df = pd.read_csv(r"D:\Programs\bluestock_mf_capstone\data\processed\clean_nav.csv")
    perf_df = pd.read_csv(r"D:\Programs\bluestock_mf_capstone\data\processed\clean_performance.csv")

    # Sort and establish daily returns
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.sort_values(['amfi_code', 'date'])
    nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()

    metrics = []
    rf_rate = 0.065 # 6.5% RBI repo rate proxy from project handbook

    for amfi, group in nav_df.groupby('amfi_code'):
        returns = group['daily_return'].dropna()
        if len(returns) < 20:
            continue

        # 1. Annualized Return & Volatility
        avg_daily_return = returns.mean()
        daily_std = returns.std()
        ann_return = (1 + avg_daily_return) ** 252 - 1
        ann_volatility = daily_std * np.sqrt(252)

        # 2. Sharpe Ratio
        sharpe = (ann_return - rf_rate) / ann_volatility if ann_volatility > 0 else 0

        # 3. Maximum Drawdown Calculation
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
    output_path = r"D:\Programs\bluestock_mf_capstone\data\processed\calculated_performance_metrics.csv"
    metrics_df.to_csv(output_path, index=False)
    print(f"Metrics calculated and exported to {output_path}")
    return metrics_df

if __name__ == "__main__":
    compute_performance_metrics()
