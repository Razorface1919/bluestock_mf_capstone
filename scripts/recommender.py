import pandas as pd
import sqlite3
from pathlib import Path

def recommend_funds(risk_appetite):
    """
    Recommends top 3 funds based on Sharpe Ratio matching the investor's risk appetite.
    Inputs: risk_appetite (str): 'Low', 'Moderate', 'High', or 'Very High'
    """
    # Resolves to the project root assuming the notebook is in a subfolder
    BASE_DIR = Path.cwd().parent
    DB_PATH = BASE_DIR / 'data' / 'db' / 'bluestock_mf.db'

    risk_appetite = risk_appetite.title()
    valid_grades = ['Low', 'Moderate', 'High', 'Very High']

    if risk_appetite not in valid_grades:
        print(f"Invalid input: '{risk_appetite}'. Choose from {valid_grades}.")
        return None

    try:
        conn = sqlite3.connect(DB_PATH)
        query = """
            SELECT d.scheme_name, d.category, d.risk_category, 
                   p.return_3yr_pct, p.sharpe_ratio, d.expense_ratio_pct
            FROM fact_performance p
            JOIN dim_fund d ON p.amfi_code = d.amfi_code
            WHERE d.risk_category = ?
            ORDER BY p.sharpe_ratio DESC
            LIMIT 3
        """
        top_3_funds = pd.read_sql(query, conn, params=(risk_appetite,))
        conn.close()

        if top_3_funds.empty:
            print(f"No funds found for risk appetite: {risk_appetite}")
            return None

        print("\n" + "="*90)
        print(f"FUND RECOMMENDATION ENGINE: Profile -> {risk_appetite} Risk")
        print("="*90)
        print(top_3_funds.to_string(index=False))
        print("="*90)

        return top_3_funds

    except Exception as e:
        print(f"Error accessing database: {e}")
        return None

if __name__ == "__main__":
    print("Testing the Recommender Engine...")
    recommend_funds('Low')
    recommend_funds('High')
