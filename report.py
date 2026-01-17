from __future__ import annotations

import numpy as np
from load_data import load_sales_csv, month_key_from_iso, compute_total_price
from analysis import group_sum_by_key, group_count_by_key


def make_report(csv_path: str) -> str:
    ts, pid, pname, qty, price, cashier, line = load_sales_csv(csv_path)
    total_price = compute_total_price(qty, price)

    total_transactions = int(qty.shape[0])
    total_units = int(qty.sum())
    total_revenue = float(total_price.sum())

    name_map = {}
    for i in range(len(pid)):
        if pid[i] not in name_map:
            name_map[pid[i]] = pname[i]

    unique_products, revenue_by_product = group_sum_by_key(pid, total_price)
    _, units_by_product = group_sum_by_key(pid, qty)

    months = month_key_from_iso(ts)
    unique_months, tx_by_month = group_count_by_key(months)
    _, units_by_month = group_sum_by_key(months, qty)
    _, revenue_by_month = group_sum_by_key(months, total_price)

    lines = []
    lines.append("Chocolate Factory — Sales Report (NumPy)")
    lines.append("=" * 45)
    lines.append(f"Transactions: {total_transactions}")
    lines.append(f"Units sold:    {total_units}")
    lines.append(f"Revenue:      ${total_revenue:,.2f}")
    lines.append("")

    lines.append("Revenue by Product")
    lines.append("-" * 45)
    for i, p in enumerate(unique_products):
        lines.append(f"{p:12s} | ${revenue_by_product[i]:10,.2f} | units={int(units_by_product[i])} | {name_map.get(p,'')}")
    lines.append("")

    lines.append("Monthly Summary")
    lines.append("-" * 45)
    for i, m in enumerate(unique_months):
        lines.append(f"{m} | tx={int(tx_by_month[i]):3d} | units={int(units_by_month[i]):4d} | ${revenue_by_month[i]:10,.2f}")

    if revenue_by_month.size:
        bm = int(np.argmax(revenue_by_month))
        lines.append("")
        lines.append(f"Best month: {unique_months[bm]} (${revenue_by_month[bm]:,.2f})")

    if revenue_by_product.size:
        bp = int(np.argmax(revenue_by_product))
        lines.append(f"Best product: {unique_products[bp]} ({name_map.get(unique_products[bp], 'Unknown')}) (${revenue_by_product[bp]:,.2f})")

    return "\n".join(lines)


def main():
    print(make_report("data/sales_log.csv"))


if __name__ == "__main__":
    main()
