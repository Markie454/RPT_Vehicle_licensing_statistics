"""Dummy data generator. Stands in for a real scraper so you can test the pipeline.

It invents figures for eight fictional clinics and saves them to data/demo.json.
Every run produces different numbers, so you can see a refresh happen.
Uses only the Python standard library, so nothing needs installing.
"""
import json
import random
from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path("data/demo.json")

CLINICS = [
    ("Riverside Clinic", "North"),
    ("Hillcrest Centre", "North"),
    ("Harbour Health", "South"),
    ("Parkview Clinic", "South"),
    ("Station Road Practice", "Midlands"),
    ("Millfield Centre", "Midlands"),
    ("Greenway Clinic", "East"),
    ("Bridgewater Practice", "East"),
]


def build_rows() -> list[dict]:
    rows = []
    for name, region in CLINICS:
        online = random.random() > 0.2
        slots = random.randint(0, 40) if online else 0
        rows.append({
            "clinic": name,
            "region": region,
            "physios": random.randint(2, 9),
            "online_booking": online,
            "slots_next_7_days": slots,
            "next_available_days": random.randint(0, 9) if slots else None,
        })
    return rows


def validate(rows: list[dict]) -> None:
    """Stop the update if the result looks wrong, rather than publish it."""
    if len(rows) != len(CLINICS):
        raise SystemExit(f"Expected {len(CLINICS)} rows, got {len(rows)}. Not saving.")


def main() -> None:
    rows = build_rows()
    validate(rows)
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%d %B %Y at %H:%M UTC"),
        "note": "Dummy data for testing. Not real.",
        "rows": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved {len(rows)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
