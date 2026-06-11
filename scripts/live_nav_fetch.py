import requests
import pandas as pd
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch_and_save_nav(scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['data'])
        df['amfi_code'] = scheme_code
        
        # Use pathlib for cross-platform compatibility (Windows \ vs Mac/Linux /)
        output_path = RAW_DATA_DIR / f"nav_{scheme_code}.csv"
        df.to_csv(output_path, index=False)
        print(f"Success: Saved {len(df)} records for {scheme_code} to {output_path}")
    else:
        print(f"Error: Failed to fetch data for {scheme_code}. Status: {response.status_code}")

if __name__ == "__main__":
    # Task 4: HDFC Top 100
    print("Fetching HDFC Top 100...")
    fetch_and_save_nav(125497)

    # Task 5: The 5 other schemes
    schemes = [119551, 120503, 118632, 119092, 120841]
    print("\nFetching additional schemes...")
    
    for code in schemes:
        fetch_and_save_nav(code)
        time.sleep(3)