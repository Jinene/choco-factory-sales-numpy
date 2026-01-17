# Chocolate Factory Sales Counter (NumPy)

This repo analyzes real (historical) chocolate factory sales data stored over several months.

## Data format
Sales are stored in `data/sales_log.csv` with columns:
- timestamp (ISO 8601)
- product_id
- product_name
- quantity
- unit_price
- cashier_id
- line_id

## Setup
```bash
pip install -r requirements.txt
Run analytics
bash
python analysis.py
Generate a clean report
bash
python report.py
