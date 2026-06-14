# Data Directory
- `/raw/`: Contains immutable, original AMFI data dumps. **Do not modify these files.**
- `/processed/`: Cleaned, merged CSVs ready for database ingestion.
- `/db/`: SQLite database storage. Note: `bluestock_mf.db` is explicitly ignored via `.gitignore` to prevent committing binary DB files. Refer to `/sql/schema.sql` for table structures.
