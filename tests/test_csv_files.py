"""Tests for saving and loading events as CSV."""

import csv
from datetime import datetime

from cartpilot.csv_files import read_events_csv, write_events_csv
from cartpilot.synthetic import DEFAULT_PRODUCTS, generate_shop

HEADER = "event_time,event_type,session_id,user_id,product_id,category,brand,price"


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


def test_save_then_load_gives_back_the_same_events(tmp_path):
    events = generate_shop(
        DEFAULT_PRODUCTS, sessions_per_product=10, start=datetime(2026, 9, 1)
    )
    path = tmp_path / "events.csv"

    write_events_csv(events, path)
    good, bad = read_events_csv(path)

    assert good == events
    assert bad == []


def test_bad_rows_are_set_aside_not_crashing(tmp_path):
    path = tmp_path / "messy.csv"
    path.write_text(
        "\n".join(
            [
                HEADER,
                "2026-09-01T10:00:00,view,s1,u1,p1,phones,,15000",
                "2026-09-01T10:01:00,banana,s2,u2,p1,phones,,15000",
                "2026-09-01T10:02:00,view,s3,u3,p1,phones,,-5",
            ]
        ),
        encoding="utf-8",
    )

    good, bad = read_events_csv(path)

    assert len(good) == 1
    assert [b.line_number for b in bad] == [3, 4]
    assert bad[0].reason.startswith("event_type")
    assert bad[1].reason.startswith("price")
