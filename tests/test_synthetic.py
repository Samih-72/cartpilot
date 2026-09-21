"""Tests for the synthetic data generator."""

import random
from datetime import datetime
from decimal import Decimal

from cartpilot.models import EventType
from cartpilot.synthetic import generate_session

START = datetime(2026, 9, 21, 10, 0)


def make_session(cart_rate, purchase_rate, seed=0):
    return generate_session(
        rng=random.Random(seed),
        session_id="s1",
        product_id="p42",
        category="phones",
        price=Decimal("15000"),
        start=START,
        cart_rate=cart_rate,
        purchase_rate=purchase_rate,
    )


def event_types(events):
    return [e.event_type for e in events]


def test_shopper_who_always_buys():
    events = make_session(cart_rate=1.0, purchase_rate=1.0)
    assert event_types(events) == [EventType.VIEW, EventType.CART, EventType.PURCHASE]


def test_shopper_who_never_carts_only_views():
    events = make_session(cart_rate=0.0, purchase_rate=1.0)
    assert event_types(events) == [EventType.VIEW]


def test_shopper_who_carts_but_never_buys():
    events = make_session(cart_rate=1.0, purchase_rate=0.0)
    assert event_types(events) == [EventType.VIEW, EventType.CART]


def test_same_seed_gives_same_result():
    first = make_session(cart_rate=0.5, purchase_rate=0.5, seed=42)
    second = make_session(cart_rate=0.5, purchase_rate=0.5, seed=42)
    assert first == second
