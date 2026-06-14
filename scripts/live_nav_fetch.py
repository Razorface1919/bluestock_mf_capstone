"""
Module: live_nav_fetch.py
Description: Interfaces with the AMFI API to fetch and store the latest NAV 
             time-series data for specified mutual fund schemes.
Author: Shubham Singh
"""

import requests
import logging
import pandas as pd
import time
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch_and_save_nav(scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data['data'])
        df['amfi_code'] = scheme_code
        
        output_path = RAW_DATA_DIR / f"nav_{scheme_code}.csv"
        df.to_csv(output_path, index=False)
        logging.info(f"Success: Saved {len(df)} records for {scheme_code} to {output_path}")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data for {scheme_code}. Error: {e}")

if __name__ == "__main__":
    target_schemes = [125497, 119551, 120503, 118632, 119092, 120841]
    
    logging.info("Initializing API fetch for target mutual fund schemes...")
    
    for code in target_schemes:
        fetch_and_save_nav(code)
        time.sleep(3) # Respectful API rate limiting