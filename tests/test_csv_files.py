"""Tests for saving events to CSV."""

import csv
from datetime import datetime

from cartpilot.csv_files import write_events_csv
from cartpilot.synthetic import DEFAULT_PRODUCTS, generate_shop


def test_write_events_csv_saves_every_event(tmp_path):
    events = generate_shop(
        DEFAULT_PRODUCTS, sessions_per_product=10, start=datetime(2026, 9, 1)
    )
    path = tmp_path / "events.csv"

    write_events_csv(events, path)

    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(events)
    assert rows[0]["event_type"] == "view"
    assert rows[0]["product_id"] == "p-phone"
    assert rows[0]["price"] == "15000"
