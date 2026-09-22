"""Tests for the synthetic data generator."""

import random
from datetime import datetime
from decimal import Decimal

from cartpilot.models import EventType
from cartpilot.synthetic import DEFAULT_PRODUCTS, generate_session, generate_shop

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


def count(events, product_id, event_type):
    return sum(
        1 for e in events if e.product_id == product_id and e.event_type == event_type
    )


# --- One shopper ---


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


# --- Whole shop ---


def test_every_product_gets_one_view_per_session():
    events = generate_shop(DEFAULT_PRODUCTS, sessions_per_product=100, start=START)
    for product in DEFAULT_PRODUCTS:
        assert count(events, product.product_id, EventType.VIEW) == 100


def test_planted_phone_problem_shows_up_in_the_data():
    events = generate_shop(DEFAULT_PRODUCTS, sessions_per_product=1000, start=START)

    phone_carts = count(events, "p-phone", EventType.CART)
    phone_buys = count(events, "p-phone", EventType.PURCHASE)
    shoe_carts = count(events, "p-shoe", EventType.CART)
    shoe_buys = count(events, "p-shoe", EventType.PURCHASE)

    # Phones: about 10% of carts become purchases. Shoes: about 60%.
    assert phone_buys / phone_carts < 0.2
    assert shoe_buys / shoe_carts > 0.45


def test_same_seed_gives_same_shop():
    first = generate_shop(DEFAULT_PRODUCTS, sessions_per_product=50, start=START)
    second = generate_shop(DEFAULT_PRODUCTS, sessions_per_product=50, start=START)
    assert first == second
