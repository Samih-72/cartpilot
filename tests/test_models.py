"""Tests for the CartPilot data models."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from cartpilot.models import Event, EventType

VALID_EVENT = {
    "event_time": "2026-09-20 10:01:00",
    "event_type": "view",
    "session_id": "s1",
    "user_id": "u7",
    "product_id": "p42",
    "category": "phones",
    "price": "15000.50",
}


def test_valid_event_is_parsed():
    event = Event(**VALID_EVENT)
    assert event.event_type is EventType.VIEW
    assert event.price == Decimal("15000.50")
    assert event.event_time.hour == 10


def test_unknown_event_type_is_rejected():
    with pytest.raises(ValidationError):
        Event(**{**VALID_EVENT, "event_type": "banana"})


def test_negative_price_is_rejected():
    with pytest.raises(ValidationError):
        Event(**{**VALID_EVENT, "price": "-5"})


def test_optional_fields_default_to_none():
    event = Event(**{k: v for k, v in VALID_EVENT.items() if k != "category"})
    assert event.category is None
    assert event.brand is None
