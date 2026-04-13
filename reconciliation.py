from decimal import Decimal


def detect_late_settlements(transactions, settlements):
    """GAP A — settlement month differs from transaction month."""
    settlement_map = {s["txn_id"]: s for s in settlements}
    issues = []

    for txn in transactions:
        txn_id = txn["txn_id"]
        if txn_id in settlement_map:
            txn_month = (txn["date"].year, txn["date"].month)
            set_month  = (settlement_map[txn_id]["settlement_date"].year,
                          settlement_map[txn_id]["settlement_date"].month)
            if txn_month != set_month:
                issues.append(
                    f"{txn_id} transacted on {txn['date']} "
                    f"but settled on {settlement_map[txn_id]['settlement_date']}"
                )

    if issues:
        print("Late Settlements Detected!")
        for msg in issues:
            print(f"  - {msg}")
    else:
        print("Late Settlements Detected! : None")


def detect_rounding_differences(transactions, settlements, tolerance=Decimal("0.01")):
    """GAP B — rounding differences visible only when totals are summed.

    Individual per-txn diffs may each be within tolerance (so they look fine),
    but the aggregate difference across all matched pairs reveals the gap.
    """
    settlement_map = {}
    for s in settlements:
        settlement_map.setdefault(s["txn_id"], Decimal("0"))
        settlement_map[s["txn_id"]] += s["settled_amount"]

    txn_map = {}
    for txn in transactions:
        txn_map.setdefault(txn["txn_id"], Decimal("0"))
        txn_map[txn["txn_id"]] += txn["amount"]

    issues = []

    for txn_id, txn_amount in txn_map.items():
        if txn_id in settlement_map:
            per_diff = abs(settlement_map[txn_id] - txn_amount)
            if Decimal("0") < per_diff <= tolerance:
                issues.append(
                    f"{txn_id} | transaction={txn_amount}, "
                    f"settled={settlement_map[txn_id]}, per-record diff={per_diff}"
                )

    if issues:
        rounding_diffs = [
            abs(settlement_map[txn_id] - amount)
            for txn_id, amount in txn_map.items()
            if txn_id in settlement_map
            and Decimal("0") < abs(settlement_map[txn_id] - amount) <= tolerance
        ]
        total_drift = sum(rounding_diffs)
        issues.append(
            f"AGGREGATE drift from rounding = {total_drift} "
            f"(each diff {rounding_diffs} looks small, but they accumulate)"
        )

    if issues:
        print("Rounding Differences Detected!")
        for msg in issues:
            print(f"  - {msg}")
    else:
        print("Rounding Differences Detected! : None")


def detect_duplicate_settlements(settlements):
    """GAP D — same txn_id settled more than once with the same amount and date."""
    seen = {}
    issues = []

    for s in settlements:
        key = (s["txn_id"], s["settlement_date"], s["settled_amount"])
        if key in seen:
            issues.append(
                f"{s['txn_id']} settled twice — "
                f"{seen[key]} and {s['settlement_id']} "
                f"both on {s['settlement_date']} for {s['settled_amount']}"
            )
        else:
            seen[key] = s["settlement_id"]

    if issues:
        print("Duplicate Settlements Detected!")
        for msg in issues:
            print(f"  - {msg}")
    else:
        print("Duplicate Settlements Detected! : None")


def detect_orphan_refunds(transactions):
    """GAP C — refund transaction references an original txn_id that does not exist."""
    txn_ids = {txn["txn_id"] for txn in transactions}
    issues = []

    for txn in transactions:
        if txn["status"] == "refunded":
            original = txn.get("refund_for")
            if original and original not in txn_ids:
                issues.append(
                    f"{txn['txn_id']} is a refund for {original} "
                    f"but {original} does not exist in transactions"
                )

    if issues:
        print("Orphan Refunds Detected!")
        for msg in issues:
            print(f"  - {msg}")
    else:
        print("Orphan Refunds Detected! : None")


if __name__ == "__main__":
    from transactions_settlements import transactions, settlements

    print("=" * 60)
    print("       RECONCILIATION REPORT")
    print("=" * 60)

    detect_late_settlements(transactions, settlements)
    print()
    detect_rounding_differences(transactions, settlements)
    print()
    detect_duplicate_settlements(settlements)
    print()
    detect_orphan_refunds(transactions)

    print("=" * 60)
