from datetime import date
from decimal import Decimal

# =============================================================================
# TRANSACTIONS dataset
# Each entry: (txn_id, date, amount, currency, merchant, status)
# =============================================================================

transactions = [
    # --- Normal matched transactions ---
    {"txn_id": "TXN001", "date": date(2024, 3, 1),  "amount": Decimal("150.00"), "currency": "USD", "merchant": "ShopMart",    "status": "completed"},
    {"txn_id": "TXN002", "date": date(2024, 3, 2),  "amount": Decimal("89.99"),  "currency": "USD", "merchant": "TechStore",   "status": "completed"},
    {"txn_id": "TXN003", "date": date(2024, 3, 5),  "amount": Decimal("200.00"), "currency": "USD", "merchant": "FoodHub",     "status": "completed"},
    {"txn_id": "TXN004", "date": date(2024, 3, 10), "amount": Decimal("45.50"),  "currency": "USD", "merchant": "GasStation",  "status": "completed"},
    {"txn_id": "TXN005", "date": date(2024, 3, 12), "amount": Decimal("310.75"), "currency": "USD", "merchant": "AirlineX",    "status": "completed"},
    {"txn_id": "TXN006", "date": date(2024, 3, 15), "amount": Decimal("22.00"),  "currency": "USD", "merchant": "CoffeeBean",  "status": "completed"},
    {"txn_id": "TXN007", "date": date(2024, 3, 18), "amount": Decimal("500.00"), "currency": "USD", "merchant": "Electronics", "status": "completed"},
    {"txn_id": "TXN008", "date": date(2024, 3, 20), "amount": Decimal("78.30"),  "currency": "USD", "merchant": "Pharmacy",    "status": "completed"},
    {"txn_id": "TXN009", "date": date(2024, 3, 22), "amount": Decimal("134.00"), "currency": "USD", "merchant": "Clothing Co", "status": "completed"},
    {"txn_id": "TXN010", "date": date(2024, 3, 25), "amount": Decimal("60.00"),  "currency": "USD", "merchant": "BookStore",   "status": "completed"},

    # GAP A — settled next month (TXN011 appears in March transactions, settlement is in April)
    {"txn_id": "TXN011", "date": date(2024, 3, 28), "amount": Decimal("250.00"), "currency": "USD", "merchant": "LuxuryGoods", "status": "completed"},

    # GAP B — rounding: three transactions that sum to a value with a 1-cent difference vs settlement
    {"txn_id": "TXN012", "date": date(2024, 3, 14), "amount": Decimal("33.335"), "currency": "USD", "merchant": "SplitPay A",  "status": "completed"},
    {"txn_id": "TXN013", "date": date(2024, 3, 14), "amount": Decimal("33.335"), "currency": "USD", "merchant": "SplitPay B",  "status": "completed"},
    {"txn_id": "TXN014", "date": date(2024, 3, 14), "amount": Decimal("33.335"), "currency": "USD", "merchant": "SplitPay C",  "status": "completed"},
    # Sum of TXN012+013+014 = 100.005 — settlement rounds to 100.01, creating a 0.005 gap

    # GAP C — refund with NO matching original transaction in the dataset
    {"txn_id": "TXN015", "date": date(2024, 3, 17), "amount": Decimal("-99.00"), "currency": "USD", "merchant": "ShopMart",    "status": "refunded",
     "refund_for": "TXN999"},  # TXN999 does not exist in this dataset

    # Normal transactions continued
    {"txn_id": "TXN016", "date": date(2024, 3, 8),  "amount": Decimal("410.00"), "currency": "USD", "merchant": "Furniture",   "status": "completed"},
    {"txn_id": "TXN017", "date": date(2024, 3, 11), "amount": Decimal("19.99"),  "currency": "USD", "merchant": "Streaming",   "status": "completed"},
    {"txn_id": "TXN018", "date": date(2024, 3, 23), "amount": Decimal("725.50"), "currency": "USD", "merchant": "Jewellery",   "status": "completed"},
    {"txn_id": "TXN019", "date": date(2024, 3, 26), "amount": Decimal("55.00"),  "currency": "USD", "merchant": "Parking",     "status": "completed"},
    {"txn_id": "TXN020", "date": date(2024, 3, 29), "amount": Decimal("180.00"), "currency": "USD", "merchant": "Restaurant",  "status": "completed"},
]


# =============================================================================
# SETTLEMENTS dataset
# Each entry: (settlement_id, txn_id, settlement_date, settled_amount, currency)
# =============================================================================

settlements = [
    # --- Normal matches ---
    {"settlement_id": "SET001", "txn_id": "TXN001", "settlement_date": date(2024, 3, 3),  "settled_amount": Decimal("150.00"), "currency": "USD"},
    {"settlement_id": "SET002", "txn_id": "TXN002", "settlement_date": date(2024, 3, 4),  "settled_amount": Decimal("89.99"),  "currency": "USD"},
    {"settlement_id": "SET003", "txn_id": "TXN003", "settlement_date": date(2024, 3, 7),  "settled_amount": Decimal("200.00"), "currency": "USD"},
    {"settlement_id": "SET004", "txn_id": "TXN004", "settlement_date": date(2024, 3, 12), "settled_amount": Decimal("45.50"),  "currency": "USD"},
    {"settlement_id": "SET005", "txn_id": "TXN005", "settlement_date": date(2024, 3, 14), "settled_amount": Decimal("310.75"), "currency": "USD"},
    {"settlement_id": "SET006", "txn_id": "TXN006", "settlement_date": date(2024, 3, 17), "settled_amount": Decimal("22.00"),  "currency": "USD"},
    {"settlement_id": "SET007", "txn_id": "TXN007", "settlement_date": date(2024, 3, 20), "settled_amount": Decimal("500.00"), "currency": "USD"},
    {"settlement_id": "SET008", "txn_id": "TXN008", "settlement_date": date(2024, 3, 22), "settled_amount": Decimal("78.30"),  "currency": "USD"},
    {"settlement_id": "SET009", "txn_id": "TXN009", "settlement_date": date(2024, 3, 24), "settled_amount": Decimal("134.00"), "currency": "USD"},
    {"settlement_id": "SET010", "txn_id": "TXN010", "settlement_date": date(2024, 3, 27), "settled_amount": Decimal("60.00"),  "currency": "USD"},

    # GAP A — TXN011 settled in APRIL (next month), not March
    {"settlement_id": "SET011", "txn_id": "TXN011", "settlement_date": date(2024, 4, 2),  "settled_amount": Decimal("250.00"), "currency": "USD"},

    # GAP B — rounding: each settled amount is rounded to 2 decimal places.
    # Individually each diff (0.005) is within tolerance, but summed they reveal a gap.
    # txn sum = 100.005, settlement sum = 100.01, aggregate diff = 0.005
    {"settlement_id": "SET012", "txn_id": "TXN012", "settlement_date": date(2024, 3, 16), "settled_amount": Decimal("33.34"), "currency": "USD"},
    {"settlement_id": "SET013", "txn_id": "TXN013", "settlement_date": date(2024, 3, 16), "settled_amount": Decimal("33.34"), "currency": "USD"},
    {"settlement_id": "SET014", "txn_id": "TXN014", "settlement_date": date(2024, 3, 16), "settled_amount": Decimal("33.33"), "currency": "USD"},

    # GAP C — refund settlement exists, but original TXN999 never appears in transactions
    {"settlement_id": "SET015", "txn_id": "TXN015", "settlement_date": date(2024, 3, 19), "settled_amount": Decimal("-99.00"), "currency": "USD"},

    # GAP D — duplicate settlement entry for TXN016 (SET016 and SET016B are both present)
    {"settlement_id": "SET016",  "txn_id": "TXN016", "settlement_date": date(2024, 3, 10), "settled_amount": Decimal("410.00"), "currency": "USD"},
    {"settlement_id": "SET016B", "txn_id": "TXN016", "settlement_date": date(2024, 3, 10), "settled_amount": Decimal("410.00"), "currency": "USD"},
    # ^ exact duplicate — same txn_id, same date, same amount

    # Normal matches continued
    {"settlement_id": "SET017", "txn_id": "TXN017", "settlement_date": date(2024, 3, 13), "settled_amount": Decimal("19.99"),  "currency": "USD"},
    {"settlement_id": "SET018", "txn_id": "TXN018", "settlement_date": date(2024, 3, 25), "settled_amount": Decimal("725.50"), "currency": "USD"},
    {"settlement_id": "SET019", "txn_id": "TXN019", "settlement_date": date(2024, 3, 28), "settled_amount": Decimal("55.00"),  "currency": "USD"},
    {"settlement_id": "SET020", "txn_id": "TXN020", "settlement_date": date(2024, 3, 31), "settled_amount": Decimal("180.00"), "currency": "USD"},
]


# =============================================================================
# RECONCILIATION GAPS REFERENCE (for your own notes — remove before submission)
# =============================================================================
# GAP A │ Cross-month settlement  │ TXN011 transacted Mar 28, settled Apr 2
# GAP B │ Rounding difference     │ TXN012+013+014 sum=100.005, SET012=100.01 (Δ0.005)
# GAP C │ Orphan refund           │ TXN015 refunds TXN999 which is not in transactions
# GAP D │ Duplicate settlement    │ SET016 and SET016B both settle TXN016 (double-payment risk)
# =============================================================================
