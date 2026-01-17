from __future__ import annotations

import numpy as np


def load_sales_csv(path: str):
    """
    Loads sales_log.csv and returns:
    - timestamps (np.ndarray[str])
    - product_id (np.ndarray[str])
    - product_name (np.ndarray[str])
    - quantity (np.ndarray[int])
    - unit_price (np.ndarray[float])
    - cashier_id (np.ndarray[str])
    - line_id (np.ndarray[str])
    """
    data = np.genfromtxt(
        path,
        delimiter=",",
        names=True,
        dtype=None,          # infer dtypes
        encoding="utf-8"
    )

    # If there is only 1 row, genfromtxt returns a 0-d record; normalize to 1-d
    if data.shape == ():
        data = np.array([data])

    timestamps = data["timestamp"].astype(str)
    product_id = data["product_id"].astype(str)
    product_name = data["product_name"].astype(str)
    quantity = data["quantity"].astype(int)
    unit_price = data["unit_price"].astype(float)
    cashier_id = data["cashier_id"].astype(str)
    line_id = data["line_id"].astype(str)

    return timestamps, product_id, product_name, quantity, unit_price, cashier_id, line_id


def month_key_from_iso(ts: np.ndarray) -> np.ndarray:
    """
    Extracts YYYY-MM from ISO timestamp strings.
    Example: 2025-09-14T10:22:11+00:00 -> 2025-09
    Works by slicing first 7 chars.
    """
    return np.char.array(ts).str[:7]


def compute_total_price(quantity: np.ndarray, unit_price: np.ndarray) -> np.ndarray:
    return quantity.astype(float) * unit_price.astype(float)
