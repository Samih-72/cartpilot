"""Tests for loading events into DuckDB."""

from datetime import datetime

from cartpilot.store import load_events
from cartpilot.synthetic import DEFAULT_PRODUCTS, generate_shop

FUNNEL = """
SELECT
    COUNT(*) FILTER (WHERE event_type = 'cart')     AS carts,
    COUNT(*) FILTER (WHERE event_type = 'purchase') AS buys
FROM events
WHERE category = ?
"""


def test_every_event_is_loaded():
    events = generate_shop(
        DEFAULT_PRODUCTS, sessions_per_product=10, start=datetime(2026, 9, 1)
    )
    con = load_events(events)

    count = con.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    assert count == len(events)


def test_sql_finds_the_planted_phone_problem():
    events = generate_shop(
        DEFAULT_PRODUCTS, sessions_per_product=200, start=datetime(2026, 9, 1)
    )
    con = load_events(events)

    phone_carts, phone_buys = con.execute(FUNNEL, ["phones"]).fetchone()
    shoe_carts, shoe_buys = con.execute(FUNNEL, ["shoes"]).fetchone()

    assert phone_buys / phone_carts < 0.3
    assert shoe_buys / shoe_carts > 0.45
