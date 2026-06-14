# Bluestock Mutual Fund Analytics Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-Star_Schema-lightgrey.svg)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Engineering-150458.svg)

## Project Overview
The **Bluestock Mutual Fund Analytics Platform** is an end-to-end data engineering and quantitative analytics platform. Built to solve severe data fragmentation in the Indian mutual fund industry, this platform automates the ingestion of public market data (AMFI, NSE, BSE), processes over 46,000 historical NAV records, and evaluates risk-adjusted performance across 40 distinct mutual fund schemes. 

This project bridges the gap between raw backend data infrastructure and executive-level business strategy, featuring a fully normalized relational database, predictive churn modeling, and an interactive Business Intelligence presentation layer.

**Key Features:**
* **Automated ETL Pipeline:** Ingests live JSON streams via REST APIs, handles business-day frequency reindexing, and scrubs null artifacts.
* **Optimized Data Architecture:** 5-table Star Schema design in SQLite (`dim_fund`, `fact_nav`, `fact_transactions`, etc.) optimized for high-speed BI querying.
* **Advanced Risk Modeling:** Computes 95% Historical Value at Risk (VaR), Conditional VaR (CVaR), and the Herfindahl-Hirschman Index (HHI) for sector concentration risk.
* **Behavioral Cohort Analytics:** Identifies at-risk capital by flagging investors with >35-day Systematic Investment Plan (SIP) transaction gaps.
* **Programmatic Recommender Engine:** Matches user risk profiles to top-performing funds optimized mathematically by Sharpe Ratio.

---

## Repository Structure

```text
.
├── dashboard/               # Power BI file (.pbix) and static dashboard exports
├── data/                    
│   ├── raw/                 # Unprocessed AMFI CSVs and JSON responses
│   ├── processed/           # Cleaned data, calculated metrics, and risk reports
│   └── db/                  # SQLite database (bluestock_mf.db) hosting the Star Schema
├── notebooks/               # Jupyter notebooks for deep EDA, cleaning, and ML cohort analysis
├── reports/                 # Executive Consulting Report (PDF), Pitch Deck, and High-Res Charts
├── scripts/                 # Core Python modules (ETL, API fetching, performance metrics)
├── sql/                     # DDL Schema definitions and advanced analytical queries
├── requirements.txt         # Python dependencies
└── run_pipeline.py          # Master execution script

```

---

## Setup Instructions

**1. Clone the Repository**
```bash
git clone https://github.com/yourusername/bluestock_mf_capstone.git
cd bluestock_mf_capstone
```

## 2. Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run the Pipeline

The project is modularized, but the entire Extract-Transform-Load (ETL) and analytics workflow can be executed sequentially using the master script.

**To run the complete pipeline:**

```bash
python run_pipeline.py
```
**To run individual modules manually:**

* **Fetch Live NAV Data:** Pulls the latest JSON data from the mfapi.in REST API.
    ```bash
    python scripts/live_nav_fetch.py
    ```

* **Execute ETL & Database Load:** Cleans raw CSVs, performs time-series forward-filling, and loads the Star Schema into `data/db/bluestock_mf.db`.
    ```bash
    python scripts/etl_pipeline.py
    ```

* **Compute Performance Metrics:** Calculates CAGR, Sharpe, Alpha, Beta, and Max Drawdown.
    ```bash
    python scripts/compute_metrics.py
    ```

* **Test Recommender Engine:** Run the terminal-based recommendation algorithm matching funds to risk appetites.
    ```bash
    python scripts/recommender.py
    ```

---

## How to Open the Dashboard

The presentation layer translates the SQLite database into interactive visual intelligence.

1. Download and install Microsoft Power BI Desktop.
2. Navigate to the `dashboard/` directory.
3. Open `bluestock_mf_dashboard.pbix`.

*Note: If database connection paths need updating, go to **Transform Data** -> **Data Source Settings** and point it to the absolute path of `data/db/bluestock_mf.db` on your local machine.*

If you do not have Power BI installed, a static, high-resolution export is available at `dashboard/Dashboard.pdf`.

---

## Key File Descriptions

* **`sql/schema.sql`:** Contains the precise DDL statements establishing the Primary/Foreign Key relationships for the 5-table Star Schema.
* **`notebooks/05_advanced_analytics.ipynb`:** Showcases the quantitative math behind the CVaR risk profiling and the >35-day SIP churn predictor.
* **`reports/Final_Report.pdf`:** A 20-page executive summary detailing the methodology, market findings, and strategic business recommendations.

---
*Prepared by Shubham Singh | June 2026*