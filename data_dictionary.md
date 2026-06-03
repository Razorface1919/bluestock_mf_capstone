# Bluestock Mutual Fund Analytics: Data Dictionary

## Dimension Tables

### `dim_fund`
List of all evaluated mutual fund schemes. 
**Source Reference:** AMFI India Public Data (`01_fund_master.csv`)
* **amfi_code (TEXT, PK):** Unique AMFI scheme identifier.
* **fund_house (TEXT):** Asset Management Company (AMC) name.
* **category / sub_category (TEXT):** Scheme classification (e.g., Equity / Large Cap).
* **expense_ratio_pct (REAL):** Annual fee charged by the AMC.
* **risk_category (TEXT):** SEBI mandated risk grading.

## Fact Tables

### `fact_nav`
Daily Net Asset Value tracking.
**Source Reference:** mfapi.in historical API (`02_nav_history.csv`)
* **amfi_code (TEXT, FK):** Reference to `dim_fund`.
* **nav_date (DATE):** Date of the NAV record (YYYY-MM-DD).
* **nav (REAL):** Closing price of the unit.
* **daily_return (REAL):** Day-over-day price change (To be calculated).

### `fact_transactions`
Individual investor actions.
**Source Reference:** Simulated behavioral dataset (`08_investor_transactions.csv`)
* **investor_id (TEXT):** Unique user identifier.
* **transaction_date (DATE):** Date the transaction was executed (YYYY-MM-DD).
* **transaction_type (TEXT):** Action taken (SIP, Lumpsum, Redemption).
* **amount_inr (REAL):** Capital moved in INR.
* **city_tier (TEXT):** T30 (Top 30 cities) vs B30 (Beyond 30).

### `fact_performance`
Calculated risk and return metrics.
**Source Reference:** Computed downstream from NAV history (`07_scheme_performance.csv`)
* **return_3yr_pct (REAL):** 3-Year CAGR.
* **alpha / beta / sharpe_ratio (REAL):** Risk-adjusted market performance metrics.
* **negative_sharpe_flag (INTEGER):** Boolean flag indicating sub-risk-free performance.