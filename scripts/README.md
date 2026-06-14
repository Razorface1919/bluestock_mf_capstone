# Execution Scripts
Contains the core Python logic for the pipeline.
- `live_nav_fetch.py`: Handles API/web scraping for latest NAVs.
- `etl_pipeline.py`: Cleans raw AMFI data and loads it into the SQLite star schema.
- `compute_metrics.py`: Calculates CAGR, Sharpe, CVaR, etc.
- `recommender.py`: Engine for risk-appetite matching.