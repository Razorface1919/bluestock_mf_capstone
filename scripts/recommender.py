import sys

def recommend_funds(risk_appetite, data_path):
    """
    Inputs:
        risk_appetite (str): Must be 'Low', 'Moderate', or 'High'
        data_path (str): Path to the performance scorecard CSV
    Output:
        Pandas DataFrame of the top 3 recommended funds.
    """
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Could not find the dataset at {data_path}")
        return None

    risk_appetite = risk_appetite.capitalize()
    valid_grades = ['Low', 'Moderate', 'High']

    if risk_appetite not in valid_grades:
        print(f"Invalid input: '{risk_appetite}'. Please choose from {valid_grades}.")
        return None

    filtered_funds = df[df['risk_grade'] == risk_appetite].copy()

    if filtered_funds.empty:
        print(f"No funds found for risk appetite: {risk_appetite}")
        return None

    top_3_funds = filtered_funds.sort_values(by='sharpe_ratio', ascending=False).head(3)

    output_columns = ['scheme_name', 'category', 'risk_grade', '3y_cagr', 'sharpe_ratio', 'expense_ratio_pct']

    actual_columns = [col for col in output_columns if col in top_3_funds.columns]

    if '3y_cagr' not in top_3_funds.columns and 'return_3yr_pct' in top_3_funds.columns:
        actual_columns = ['scheme_name', 'category', 'risk_grade', 'return_3yr_pct', 'sharpe_ratio', 'expense_ratio_pct']

    top_3_funds = top_3_funds[actual_columns]

    print("\n" + "="*90)
    print(f"FUND RECOMMENDATION ENGINE: Profile -> {risk_appetite} Risk")
    print("="*90)
    print(top_3_funds.to_string(index=False))
    print("="*90)

    return top_3_funds

# --- Execution Example ---
file_path = r"D:\Programs\bluestock_mf_capstone\data\processed\clean_performance.csv"

print("Testing the Recommender Engine...")

# Test 1: Conservative Investor
low_risk_recs = recommend_funds('Low', data_path=file_path)

# Test 2: Aggressive Investor
high_risk_recs = recommend_funds('High', data_path=file_path)
