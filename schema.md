# Chocolate Factory Sales Log Schema (CSV)

File: data/sales_log.csv

Columns:
- timestamp (ISO 8601) e.g. 2025-09-14T10:22:11+00:00
- product_id (string) e.g. DARK_70
- product_name (string) e.g. Dark Chocolate 70%
- quantity (int)
- unit_price (float)
- cashier_id (string)
- line_id (string)

Notes:
- total_price is computed: quantity * unit_price
- timestamp is used for monthly aggregation
