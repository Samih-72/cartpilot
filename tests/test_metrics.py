"""Tests for the shop metrics."""

from datetime import datetime
from decimal import Decimal

import pytest

from cartpilot.metrics import funnel_by_category
from cartpilot.store import load_events
from cartpilot.synthetic import DEFAULT_PRODUCTS, generate_shop


@pytest.fixture(scope="module")
def funnels():
    """Build the pretend shop once, and share it with every test in this file."""
    events = generate_shop(
        DEFAULT_PRODUCTS, sessions_per_product=200, start=datetime(2026, 9, 1)
    )
    return {f.category: f for f in funnel_by_category(load_events(events))}


def test_every_category_is_reported(funnels):
    assert set(funnels) == {"phones", "shoes", "books"}


def test_every_viewer_is_counted(funnels):
    for funnel in funnels.values():
        assert funnel.views == 200


def test_phones_have_the_worst_purchase_rate(funnels):
    assert funnels["phones"].purchase_rate < 0.3
    assert funnels["shoes"].purchase_rate > 0.45


def test_phones_leave_the_most_money_in_carts(funnels):
    worst = max(funnels.values(), key=lambda f: f.abandoned_value)
    assert worst.category == "phones"


def test_revenue_matches_the_number_of_purchases(funnels):
    phones = funnels["phones"]
    assert phones.revenue == phones.purchases * Decimal("15000")
