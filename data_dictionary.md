# Bluestock Mutual Fund Analytics: Data Dictionary

## Dimension Tables

### `dim_fund`
List of all evaluated mutual fund schemes. 
**Source Reference:** AMFI India Public Data (`01_fund_master.csv`)
* **amfi_code (TEXT, PK):** Unique AMFI scheme identifier.
* **fund_house (TEXT):** Asset Management Company (AMC) name.
* **scheme_name (TEXT):** Full official AMFI scheme name.
* **category / sub_category (TEXT):** Scheme classification (e.g., Equity / Large Cap).
* **expense_ratio_pct (REAL):** Annual fee charged by the AMC.
* **risk_category (TEXT):** SEBI mandated risk grading.

### `dim_date`
Programmatically generated time-intelligence calendar.
**Source Reference:** Python `pd.date_range` mapping
* **date_id (INTEGER, PK):** Integer representation of date (YYYYMMDD).
* **date (DATE):** Standard date string (YYYY-MM-DD).
* **year / month / quarter (INTEGER):** Extracted chronological units.
* **is_weekday (BOOLEAN):** Flag for standard trading days.

## Fact Tables

### `fact_nav`
Daily Net Asset Value tracking.
**Source Reference:** mfapi.in historical API (`02_nav_history.csv`)
* **amfi_code (TEXT, FK):** Reference to `dim_fund`.
* **nav_date (DATE):** Date of the NAV record (YYYY-MM-DD).
* **nav (REAL):** Closing price of the unit.
* **daily_return (REAL):** Day-over-day price change.

### `fact_transactions`
Individual investor actions.
**Source Reference:** Simulated behavioral dataset (`08_investor_transactions.csv`)
* **transaction_id (INTEGER, PK):** Auto-incrementing unique key.
* **investor_id (TEXT):** Unique user identifier.
* **transaction_date (DATE):** Date the transaction was executed (YYYY-MM-DD).
* **transaction_type (TEXT):** Action taken (SIP, Lumpsum, Redemption).
* **amount_inr (REAL):** Capital moved in INR.
* **city_tier (TEXT):** T30 (Top 30 cities) vs B30 (Beyond 30).

### `fact_performance`
Calculated risk and return metrics.
**Source Reference:** Computed downstream from NAV history (`07_scheme_performance.csv`)
* **amfi_code (TEXT, PK):** Reference to `dim_fund`.
* **return_1yr_pct / return_3yr_pct / return_5yr_pct (REAL):** CAGR and absolute returns.
* **benchmark_3yr_pct (REAL):** Benchmark index comparison metric.
* **alpha / beta / sharpe_ratio / sortino_ratio (REAL):** Risk-adjusted market performance metrics.
* **std_dev_ann_pct / max_drawdown_pct (REAL):** Downside and volatility risk metrics.

### `fact_aum`
Quarterly Asset Under Management snapshots by fund house.
**Source Reference:** AMFI Quarterly Reports (`03_aum_by_fund_house.csv`)
* **fund_house (TEXT):** AMC name matching `dim_fund`.
* **date (DATE):** Snapshot date (YYYY-MM-DD).
* **aum_crore (REAL):** Total assets managed in Crores (INR).
* **num_schemes (INTEGER):** Total number of active schemes managed.