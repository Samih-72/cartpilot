"""Tests for the diagnostics rules."""

from datetime import datetime
from decimal import Decimal

import pytest

from cartpilot.diagnostics import CART_ABANDONMENT, find_cart_abandonment
from cartpilot.metrics import CategoryFunnel, funnel_by_category
from cartpilot.store import load_events
from cartpilot.synthetic import DEFAULT_PRODUCTS, generate_shop


def make_funnel(category, views, carts, purchases, price):
    """Build a funnel by hand, for tests that need exact numbers."""
    return CategoryFunnel(
        category=category,
        views=views,
        carts=carts,
        purchases=purchases,
        revenue=Decimal(price) * purchases,
        abandoned_value=Decimal(price) * (carts - purchases),
    )


@pytest.fixture(scope="module")
def shop_funnels():
    events = generate_shop(
        DEFAULT_PRODUCTS, sessions_per_product=200, start=datetime(2026, 9, 1)
    )
    return funnel_by_category(load_events(events))


def test_phones_are_flagged_in_the_pretend_shop(shop_funnels):
    findings = find_cart_abandonment(shop_funnels)

    assert [f.subject for f in findings] == ["phones"]
    assert findings[0].rule == CART_ABANDONMENT
    assert findings[0].money_at_risk > 0


def test_a_healthy_shop_has_no_findings():
    funnels = [
        make_funnel("phones", views=500, carts=200, purchases=120, price=15000),
        make_funnel("shoes", views=500, carts=200, purchases=110, price=2500),
        make_funnel("books", views=500, carts=200, purchases=130, price=400),
    ]

    assert find_cart_abandonment(funnels) == []


def test_tiny_categories_are_ignored():
    funnels = [
        make_funnel("phones", views=500, carts=200, purchases=120, price=15000),
        make_funnel("socks", views=20, carts=5, purchases=0, price=200),
    ]

    assert find_cart_abandonment(funnels) == []
