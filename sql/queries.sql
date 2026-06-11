-- 1. Top 5 Fund Houses by AUM 
SELECT fund_house, aum_crore 
FROM fact_aum 
WHERE date = (SELECT MAX(date) FROM fact_aum)
ORDER BY aum_crore DESC 
LIMIT 5;

-- 2. Average NAV per month 
SELECT d.year, d.month, ROUND(AVG(n.nav), 2) AS avg_nav_inr
FROM fact_nav n
JOIN dim_date d ON n.nav_date = d.date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 3. SIP Inflow Year-over-Year (YoY) Total 
SELECT d.year, SUM(t.amount_inr) AS total_sip_inflow_inr
FROM fact_transactions t
JOIN dim_date d ON t.transaction_date = d.date
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year;

-- 4. Total transaction volume and value by state
SELECT state, COUNT(investor_id) AS total_transactions, ROUND(SUM(amount_inr), 2) AS total_volume_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_volume_inr DESC;

-- 5. Highly efficient funds: Expense ratio strictly < 1%
SELECT amfi_code, scheme_name, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- 6. Top 5 schemes by 3-Year Return outperforming their benchmark
SELECT f.scheme_name, p.return_3yr_pct, p.benchmark_3yr_pct, p.alpha
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.alpha > 0
ORDER BY p.return_3yr_pct DESC
LIMIT 5;

-- 7. Investor demographics: Average SIP amount by Age Group
SELECT age_group, ROUND(AVG(amount_inr), 2) AS avg_sip_amount_inr
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY age_group
ORDER BY avg_sip_amount_inr DESC;

-- 8. Transaction concentration: T30 vs B30 cities
SELECT city_tier, COUNT(*) AS tx_count, SUM(amount_inr) AS total_inflow_inr
FROM fact_transactions
GROUP BY city_tier;

-- 9. Risk Analysis: Funds with a negative Sharpe Ratio 
SELECT f.scheme_name, f.risk_category, p.sharpe_ratio, p.return_1yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.sharpe_ratio < 0
ORDER BY p.sharpe_ratio ASC;

-- 10. AMC Market Share: Total AUM managed per Fund House
SELECT fund_house, MAX(aum_crore) AS latest_aum_crore
FROM fact_aum
WHERE date = (SELECT MAX(date) FROM fact_aum)
GROUP BY fund_house
ORDER BY latest_aum_crore DESC;