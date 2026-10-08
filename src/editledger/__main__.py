"""Record four events, then show the chain check."""

from __future__ import annotations

from .engine import Ledger, format_report


def build() -> Ledger:
    ledger = Ledger()
    ledger.append("parental_stock", {"vial": "HEK-P-014"})
    ledger.append("edit", {"editor": "ABE8e", "guide": "g.12"})
    ledger.append("clone_pick", {"well": "B4"})
    ledger.append("passage", {"passage": "12"})
    return ledger


def main() -> int:
    ledger = build()
    print(format_report(ledger))
    print("")
    print("after a silent rewrite of the guide:")
    event = ledger.events[1]
    payload = event["payload"]
    assert isinstance(payload, dict)
    payload["guide"] = "g.99"
    print(format_report(ledger))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
