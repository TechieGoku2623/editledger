"""Each event stores the hash of the event before it.

Recomputing the chain from the first event is the tamper check.
"""

from __future__ import annotations

import hashlib
import json
from typing import Mapping


class LedgerError(ValueError):
    """An event is missing the object it has to name."""


class Ledger:
    def __init__(self) -> None:
        self.events: list[dict[str, object]] = []

    def append(self, kind: str, payload: Mapping[str, object]) -> dict[str, object]:
        clean = _payload(kind, payload)
        previous = "" if not self.events else str(self.events[-1]["hash"])
        digest = _digest(previous, kind, clean)
        record = {"kind": kind, "payload": clean, "prev": previous, "hash": digest}
        self.events.append(record)
        return record

    def verify(self) -> dict[str, object]:
        previous = ""
        for index, event in enumerate(self.events):
            kind = str(event["kind"])
            payload = event["payload"]
            assert isinstance(payload, dict)
            expected = _digest(previous, kind, payload)
            if event.get("prev") != previous or event.get("hash") != expected:
                return {"intact": False, "broken_at": index}
            previous = expected
        return {"intact": True, "broken_at": None, "events": len(self.events)}


def format_report(ledger: Ledger) -> str:
    check = ledger.verify()
    lines = ["editledger", ""]
    for index, event in enumerate(ledger.events, start=1):
        payload = event["payload"]
        assert isinstance(payload, dict)
        detail = ", ".join(f"{key}={value}" for key, value in payload.items())
        lines.append(f"{index}. {event['kind']}  {detail}")
        lines.append(f"   hash {str(event['hash'])[:12]}")
    lines.append("")
    lines.append(f"chain intact: {str(check['intact']).lower()}")
    return "\n".join(lines)


def _payload(kind: str, payload: Mapping[str, object]) -> dict[str, str]:
    required = {
        "parental_stock": ("vial",),
        "edit": ("editor", "guide"),
        "clone_pick": ("well",),
        "passage": ("passage",),
    }.get(kind)
    if required is None:
        raise LedgerError("unknown event kind")
    clean: dict[str, str] = {}
    for key in required:
        value = str(payload.get(key, "")).strip()
        if not value:
            raise LedgerError(f"{kind} requires {key}")
        clean[key] = value
    return clean


def _digest(previous: str, kind: str, payload: Mapping[str, str]) -> str:
    body = json.dumps(
        {"prev": previous, "kind": kind, "payload": dict(payload)},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(body.encode()).hexdigest()
