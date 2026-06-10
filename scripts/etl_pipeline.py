import os
import pandas as pd
import sqlite3

DB_PATH = r"D:\Programs\bluestock_mf_capstone\data\processed\bluestock_mf.db"
RAW_DIR = r"D:\Programs\bluestock_mf_capstone\data\raw"
PROCESSED_DIR = r"D:\Programs\bluestock_mf_capstone\data\processed"

def clean_and_load_pipeline():
    print("Starting Master ETL Pipeline...")
    conn = sqlite3.connect(DB_PATH)

    # 1. Clean & Load NAV History
    print("Processing NAV History...")
    nav_df = pd.read_csv(os.path.join(RAW_DIR, "02_nav_history.csv"))
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.sort_values(['amfi_code', 'date'])
    nav_df['nav'] = pd.to_numeric(nav_df['nav'], errors='coerce')
    nav_df = nav_df.dropna(subset=['nav'])
    nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'])
    # Forward-fill holiday gaps
    nav_df['nav'] = nav_df.groupby('amfi_code')['nav'].ffill()
    nav_df.to_csv(os.path.join(PROCESSED_DIR, "clean_nav.csv"), index=False)
    nav_df.to_sql("fact_nav", conn, if_exists="replace", index=False)

    # 2. Clean & Load Investor Transactions
    print("Processing Transactions...")
    tx_df = pd.read_csv(os.path.join(RAW_DIR, "clean_transactions.csv")) # Using existing or raw base
    tx_df['transaction_date'] = pd.to_datetime(tx_df['transaction_date'])
    tx_df.to_sql("fact_transactions", conn, if_exists="replace", index=False)

    # 3. Clean & Load Performance Scorecard
    print("Processing Fund Performance...")
    perf_df = pd.read_csv(os.path.join(RAW_DIR, "clean_performance.csv"))
    perf_df.to_sql("fact_performance", conn, if_exists="replace", index=False)

    print("Master ETL completed successfully. Database synced!")
    conn.close()

if __name__ == "__main__":
    clean_and_load_pipeline()
