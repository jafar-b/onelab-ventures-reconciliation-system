import unittest
from datetime import date
from decimal import Decimal

from reconciliation import (
    detect_late_settlements,
    detect_rounding_differences,
    detect_duplicate_settlements,
    detect_orphan_refunds,
)


# Helper: capture print output so we can assert on it
from io import StringIO
import sys

def run_and_capture(func, *args):
    buf = StringIO()
    sys.stdout = buf
    func(*args)
    sys.stdout = sys.__stdout__
    return buf.getvalue()


# =============================================================================
# GAP A — Late / cross-month settlements
# =============================================================================

class TestLateSettlements(unittest.TestCase):

    def test_detects_settlement_in_next_month(self):
        """Transaction in March settled in April should be flagged."""
        txns = [
            {"txn_id": "T1", "date": date(2024, 3, 28), "amount": Decimal("100"), "status": "completed"}
        ]
        sets = [
            {"settlement_id": "S1", "txn_id": "T1", "settlement_date": date(2024, 4, 2), "settled_amount": Decimal("100")}
        ]
        output = run_and_capture(detect_late_settlements, txns, sets)
        self.assertIn("Late Settlements Detected!", output)
        self.assertIn("T1", output)

    def test_same_month_settlement_is_clean(self):
        """Transaction and settlement in the same month should not be flagged."""
        txns = [
            {"txn_id": "T1", "date": date(2024, 3, 1), "amount": Decimal("100"), "status": "completed"}
        ]
        sets = [
            {"settlement_id": "S1", "txn_id": "T1", "settlement_date": date(2024, 3, 5), "settled_amount": Decimal("100")}
        ]
        output = run_and_capture(detect_late_settlements, txns, sets)
        self.assertIn("None", output)
        self.assertNotIn("T1\n", output)

    def test_no_settlement_at_all_does_not_crash(self):
        """Transaction with no settlement entry should not crash or flag a late settlement."""
        txns = [
            {"txn_id": "T1", "date": date(2024, 3, 1), "amount": Decimal("50"), "status": "completed"}
        ]
        output = run_and_capture(detect_late_settlements, txns, [])
        self.assertIn("None", output)


# =============================================================================
# GAP B — Rounding differences
# =============================================================================

class TestRoundingDifferences(unittest.TestCase):

    def test_detects_small_per_record_rounding_diff(self):
        """A settled amount 0.005 away from the transaction should be flagged."""
        txns = [
            {"txn_id": "T1", "amount": Decimal("33.335"), "date": date(2024, 3, 1), "status": "completed"}
        ]
        sets = [
            {"settlement_id": "S1", "txn_id": "T1", "settlement_date": date(2024, 3, 2), "settled_amount": Decimal("33.34")}
        ]
        output = run_and_capture(detect_rounding_differences, txns, sets)
        self.assertIn("Rounding Differences Detected!", output)
        self.assertIn("T1", output)

    def test_detects_aggregate_drift_across_multiple_records(self):
        """Three records each with a 0.005 diff should show aggregate drift of 0.015."""
        txns = [
            {"txn_id": "T1", "amount": Decimal("33.335"), "date": date(2024, 3, 1), "status": "completed"},
            {"txn_id": "T2", "amount": Decimal("33.335"), "date": date(2024, 3, 1), "status": "completed"},
            {"txn_id": "T3", "amount": Decimal("33.335"), "date": date(2024, 3, 1), "status": "completed"},
        ]
        sets = [
            {"settlement_id": "S1", "txn_id": "T1", "settlement_date": date(2024, 3, 2), "settled_amount": Decimal("33.34")},
            {"settlement_id": "S2", "txn_id": "T2", "settlement_date": date(2024, 3, 2), "settled_amount": Decimal("33.34")},
            {"settlement_id": "S3", "txn_id": "T3", "settlement_date": date(2024, 3, 2), "settled_amount": Decimal("33.33")},
        ]
        output = run_and_capture(detect_rounding_differences, txns, sets)
        self.assertIn("AGGREGATE", output)
        self.assertIn("0.015", output)

    def test_exact_match_is_clean(self):
        """Identical transaction and settled amounts should not be flagged."""
        txns = [
            {"txn_id": "T1", "amount": Decimal("100.00"), "date": date(2024, 3, 1), "status": "completed"}
        ]
        sets = [
            {"settlement_id": "S1", "txn_id": "T1", "settlement_date": date(2024, 3, 2), "settled_amount": Decimal("100.00")}
        ]
        output = run_and_capture(detect_rounding_differences, txns, sets)
        self.assertIn("None", output)

    def test_large_diff_is_not_flagged_as_rounding(self):
        """A large discrepancy (e.g. $50) is not a rounding issue and should not appear."""
        txns = [
            {"txn_id": "T1", "amount": Decimal("150.00"), "date": date(2024, 3, 1), "status": "completed"}
        ]
        sets = [
            {"settlement_id": "S1", "txn_id": "T1", "settlement_date": date(2024, 3, 2), "settled_amount": Decimal("100.00")}
        ]
        output = run_and_capture(detect_rounding_differences, txns, sets)
        self.assertIn("None", output)


# =============================================================================
# GAP C — Orphan refunds
# =============================================================================

class TestOrphanRefunds(unittest.TestCase):

    def test_detects_refund_with_missing_original(self):
        """A refund pointing to a txn_id not in the dataset should be flagged."""
        txns = [
            {"txn_id": "T1", "amount": Decimal("-50.00"), "date": date(2024, 3, 5),
             "status": "refunded", "refund_for": "T999"}
        ]
        output = run_and_capture(detect_orphan_refunds, txns)
        self.assertIn("Orphan Refunds Detected!", output)
        self.assertIn("T999", output)

    def test_refund_with_valid_original_is_clean(self):
        """A refund whose original transaction exists should not be flagged."""
        txns = [
            {"txn_id": "T1", "amount": Decimal("100.00"), "date": date(2024, 3, 1), "status": "completed"},
            {"txn_id": "T2", "amount": Decimal("-100.00"), "date": date(2024, 3, 5),
             "status": "refunded", "refund_for": "T1"},
        ]
        output = run_and_capture(detect_orphan_refunds, txns)
        self.assertIn("None", output)

    def test_no_refunds_at_all_is_clean(self):
        """Dataset with no refunds should produce no issues."""
        txns = [
            {"txn_id": "T1", "amount": Decimal("75.00"), "date": date(2024, 3, 1), "status": "completed"}
        ]
        output = run_and_capture(detect_orphan_refunds, txns)
        self.assertIn("None", output)


# =============================================================================
# GAP D — Duplicate settlements
# =============================================================================

class TestDuplicateSettlements(unittest.TestCase):

    def test_detects_exact_duplicate(self):
        """Two settlement records with same txn_id, date, and amount should be flagged."""
        sets = [
            {"settlement_id": "S1", "txn_id": "T1", "settlement_date": date(2024, 3, 10), "settled_amount": Decimal("410.00")},
            {"settlement_id": "S2", "txn_id": "T1", "settlement_date": date(2024, 3, 10), "settled_amount": Decimal("410.00")},
        ]
        output = run_and_capture(detect_duplicate_settlements, sets)
        self.assertIn("Duplicate Settlements Detected!", output)
        self.assertIn("T1", output)

    def test_same_txn_different_date_is_clean(self):
        """Same txn_id settled on two different dates is not a duplicate."""
        sets = [
            {"settlement_id": "S1", "txn_id": "T1", "settlement_date": date(2024, 3, 10), "settled_amount": Decimal("410.00")},
            {"settlement_id": "S2", "txn_id": "T1", "settlement_date": date(2024, 3, 11), "settled_amount": Decimal("410.00")},
        ]
        output = run_and_capture(detect_duplicate_settlements, sets)
        self.assertIn("None", output)

    def test_unique_settlements_are_clean(self):
        """All unique settlement records should produce no issues."""
        sets = [
            {"settlement_id": "S1", "txn_id": "T1", "settlement_date": date(2024, 3, 1), "settled_amount": Decimal("100.00")},
            {"settlement_id": "S2", "txn_id": "T2", "settlement_date": date(2024, 3, 2), "settled_amount": Decimal("200.00")},
        ]
        output = run_and_capture(detect_duplicate_settlements, sets)
        self.assertIn("None", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
