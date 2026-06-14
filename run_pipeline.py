"""
Bluestock Mutual Fund Analytics - Master Execution Script
Author: Shubham Singh
Description: Orchestrates the end-to-end data pipeline from ingestion to risk modeling.
"""

import subprocess
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)

# Define absolute paths dynamically
BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR / "scripts"

# Define the precise execution order
PIPELINE_STEPS = [
    ("Fetching Live NAV Data", "live_nav_fetch.py"),
    ("Running ETL & DB Ingestion", "etl_pipeline.py"),
    ("Computing Performance Metrics", "compute_metrics.py"),
    ("Generating Recommendations", "recommender.py")
]

def run_script(script_name: str, step_description: str):
    """Executes a Python script as a subprocess with error handling."""
    script_path = SCRIPTS_DIR / script_name
    
    if not script_path.exists():
        logging.error(f"File not found: {script_path}")
        sys.exit(1)
        
    logging.info(f"STARTING: {step_description} ({script_name})...")
    
    try:
        # Run the script and capture output
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            text=True,
            capture_output=True
        )
        logging.info(f"SUCCESS: {script_name} completed.\n{result.stdout.strip()}")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"FAILED: {script_name} encountered an error.\n{e.stderr.strip()}")
        sys.exit(1) 

def main():
    logging.info("Initializing Bluestock MF Capstone Pipeline...")
    logging.info("-" * 50)
    
    for description, script in PIPELINE_STEPS:
        run_script(script, description)
        logging.info("-" * 50)
        
    logging.info("Pipeline Execution Complete. Data is ready for the BI Dashboard.")

if __name__ == "__main__":
    main()