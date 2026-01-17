from __future__ import annotations

import numpy as np
from load_data import load_sales_csv, month_key_from_iso, compute_total_price


def group_sum_by_key(keys: np.ndarray, values: np.ndarray):
    """
    Groups values by keys and sums them.
    Returns (unique_keys, summed_values) sorted by unique_keys.
    """
    unique_keys, inv = np.unique(keys, return_inverse=True)
    sums = np.zeros(unique_keys.shape[0], dtype=float)
    np.add.at(sums, inv, values.astype(float))
    return unique_keys, sums


def group_count_by_key(keys: np.ndarray):
    """
    Counts rows per key.
    Returns (unique_keys, counts) sorted by unique_keys.
    """
    unique_keys, inv = np.unique(keys, return_inverse=True)
    counts = np.zeros(unique_keys.shape[0], dtype=int)
    np.add.at(counts, inv, 1)
    return unique_keys, counts


def main():
    path = "data/sales_log.csv"
    ts, pid, pname, qty, price, cashier, line = load_sales_csv(path)
    total_price = compute_total_price(qty, price)

    # Global KPIs
    total_transactions = int(qty.shape[0])
    total_units = int(qty.sum())
    total_revenue = float(total_price.sum())

    # Per-product
    product_key = pid  # stable key
    _, units_by_product = group_sum_by_key(product_key, qty)
    unique_products, revenue_by_product = group_sum_by_key(product_key, total_price)

    # Map product_id -> product_name (first occurrence)
    # (Assumes product_name is consistent for same product_id)
    name_map = {}
    for i in range(len(pid)):
        if pid[i] not in name_map:
            name_map[pid[i]] = pname[i]

    # Monthly
    months = month_key_from_iso(ts)
    unique_months, tx_by_month = group_count_by_key(months)
    _, units_by_month = group_sum_by_key(months, qty)
    _, revenue_by_month = group_sum_by_key(months, total_price)

    # Bests
    best_month_idx = int(np.argmax(revenue_by_month)) if revenue_by_month.size else -1
    best_product_idx = int(np.argmax(revenue_by_product)) if revenue_by_product.size else -1

    print("=== Chocolate Factory Sales Analytics (NumPy) ===\n")
    print(f"Transactions: {total_transactions}")
    print(f"Units sold:    {total_units}")
    print(f"Revenue:      ${total_revenue:,.2f}\n")

    print("=== Revenue by Product ===")
    for i, p in enumerate(unique_products):
        print(f"- {p} ({name_map.get(p, 'Unknown')}): ${revenue_by_product[i]:,.2f} | units={int(units_by_product[i])}")
    print()

    print("=== Monthly Summary ===")
    for i, m in enumerate(unique_months):
        print(f"- {m}: transactions={int(tx_by_month[i])}, units={int(units_by_month[i])}, revenue=${revenue_by_month[i]:,.2f}")
    print()

    if best_month_idx >= 0:
        print(f"Best month (by revenue): {unique_months[best_month_idx]} (${revenue_by_month[best_month_idx]:,.2f})")
    if best_product_idx >= 0:
        bp = unique_products[best_product_idx]
        print(f"Best product (by revenue): {bp} ({name_map.get(bp, 'Unknown')}) (${revenue_by_product[best_product_idx]:,.2f})")


if __name__ == "__main__":
    main()
