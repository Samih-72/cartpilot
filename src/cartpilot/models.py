"""Core data models for CartPilot."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """The shopper actions CartPilot understands."""

    VIEW = "view"
    CART = "cart"
    REMOVE_FROM_CART = "remove_from_cart"
    PURCHASE = "purchase"


class Event(BaseModel):
    """A single shopper action on a product."""

    event_time: datetime
    event_type: EventType
    session_id: str
    user_id: str
    product_id: str
    category: str | None = None
    brand: str | None = None
    price: Decimal = Field(ge=0)
