import os
import pandas as pd
import sqlite3
from pathlib import Path

# 1. Dynamic Path Resolution
BASE_DIR = Path(__file__).resolve().parent.parent 
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_PATH = PROCESSED_DIR / "bluestock_mf.db"

def clean_and_load_pipeline():
    print("Starting Master ETL Pipeline...")
    conn = sqlite3.connect(DB_PATH)

    # 1. Cleaning & Load NAV History
    print("Processing NAV History...")
    nav_df = pd.read_csv(RAW_DIR / "02_nav_history.csv")
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.sort_values(['amfi_code', 'date'])
    nav_df['nav'] = pd.to_numeric(nav_df['nav'], errors='coerce')
    nav_df = nav_df.dropna(subset=['nav'])
    nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'])
    
    # 2. Applying Business Day Reindexing & FFill
    print("Aligning trading days and forward-filling NAV...")
    nav_df = nav_df.set_index('date')
    nav_df = nav_df.groupby('amfi_code')['nav'].resample('B').ffill().reset_index()
    
    nav_df.to_csv(PROCESSED_DIR / "clean_nav.csv", index=False)
    nav_df.to_sql("fact_nav", conn, if_exists="replace", index=False)

    # 3. Cleaning & Load Investor Transactions
    print("Processing Transactions...")
    tx_df = pd.read_csv(RAW_DIR / "clean_transactions.csv") 
    tx_df['transaction_date'] = pd.to_datetime(tx_df['transaction_date'])
    tx_df.to_sql("fact_transactions", conn, if_exists="replace", index=False)

    # 4. Cleaning & Load Performance Scorecard
    print("Processing Fund Performance...")
    perf_df = pd.read_csv(RAW_DIR / "clean_performance.csv")
    perf_df.to_sql("fact_performance", conn, if_exists="replace", index=False)

    print("Master ETL completed successfully. Database synced!")
    conn.close()

if __name__ == "__main__":
    clean_and_load_pipeline()
