"""A rewritten guide breaks the chain. A nickname-only stock does not append."""

from __future__ import annotations

import unittest

from editledger import Ledger, LedgerError
from editledger.__main__ import build


class LedgerTests(unittest.TestCase):
    def test_four_events_verify(self) -> None:
        check = build().verify()
        self.assertTrue(check["intact"])
        self.assertEqual(check["events"], 4)

    def test_rewriting_a_past_guide_is_detected(self) -> None:
        ledger = build()
        payload = ledger.events[1]["payload"]
        assert isinstance(payload, dict)
        payload["guide"] = "g.99"
        check = ledger.verify()
        self.assertFalse(check["intact"])
        self.assertEqual(check["broken_at"], 1)

    def test_edit_without_a_guide_raises(self) -> None:
        ledger = Ledger()
        with self.assertRaises(LedgerError):
            ledger.append("edit", {"editor": "ABE8e"})

    def test_parental_stock_needs_a_vial(self) -> None:
        ledger = Ledger()
        with self.assertRaises(LedgerError):
            ledger.append("parental_stock", {"nickname": "parent"})


if __name__ == "__main__":
    unittest.main()
