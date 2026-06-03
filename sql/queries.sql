-- sql/queries.sql

-- 1. Top 5 funds by AUM
SELECT scheme_name, fund_house, category, aum_crore 
FROM fact_performance 
ORDER BY aum_crore DESC 
LIMIT 5;

-- 2. Average NAV per month (Using dim_date for time-series aggregation)
SELECT d.year, d.month_name, ROUND(AVG(n.nav), 2) as avg_nav
FROM fact_nav n
JOIN dim_date d ON n.nav_date = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 3. SIP Inflow Year-over-Year (YoY) Total
SELECT d.year, SUM(t.amount_inr) as total_sip_inflow
FROM fact_transactions t
JOIN dim_date d ON t.transaction_date = d.date_id
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year;

-- 4. Total transaction volume and value by state
SELECT state, COUNT(investor_id) as total_transactions, ROUND(SUM(amount_inr), 2) as total_volume_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_volume_inr DESC;

-- 5. Highly efficient funds: Expense ratio strictly < 1%
SELECT amfi_code, scheme_name, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- 6. Top 5 schemes by 3-Year Return outperforming their benchmark
SELECT scheme_name, return_3yr_pct, benchmark_3yr_pct, alpha
FROM fact_performance
WHERE alpha > 0
ORDER BY return_3yr_pct DESC
LIMIT 5;

-- 7. Investor demographics: Average SIP amount by Age Group
SELECT age_group, ROUND(AVG(amount_inr), 2) as avg_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY age_group
ORDER BY avg_sip_amount DESC;

-- 8. Transaction concentration: T30 vs B30 cities
SELECT city_tier, COUNT(*) as tx_count, SUM(amount_inr) as total_inflow
FROM fact_transactions
GROUP BY city_tier;

-- 9. Risk Analysis: Funds with a negative Sharpe Ratio
SELECT p.scheme_name, f.risk_category, p.sharpe_ratio, p.return_1yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.negative_sharpe_flag = 1
ORDER BY p.sharpe_ratio ASC;

-- 10. AMC Market Share: Total AUM managed per Fund House
SELECT fund_house, SUM(aum_crore) as total_amc_aum
FROM fact_performance
GROUP BY fund_house
ORDER BY total_amc_aum DESC;