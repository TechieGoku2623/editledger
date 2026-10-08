"""Append-only lineage. A rewritten event fails the chain check."""

from .engine import Ledger, LedgerError

__all__ = ["Ledger", "LedgerError"]
