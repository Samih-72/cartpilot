"""Generate fake shop events with known, planted problems (for testing)."""

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from cartpilot.models import Event, EventType


@dataclass(frozen=True)
class ProductSpec:
    """A product in the fake shop, with the funnel rates we want to plant."""

    product_id: str
    category: str
    price: Decimal
    cart_rate: float
    purchase_rate: float


# The phone has a planted problem: many add to cart, but 90% leave without buying.
DEFAULT_PRODUCTS = [
    ProductSpec(
        product_id="p-phone",
        category="phones",
        price=Decimal("15000"),
        cart_rate=0.40,
        purchase_rate=0.10,
    ),
    ProductSpec(
        product_id="p-shoe",
        category="shoes",
        price=Decimal("2500"),
        cart_rate=0.30,
        purchase_rate=0.60,
    ),
    ProductSpec(
        product_id="p-book",
        category="books",
        price=Decimal("400"),
        cart_rate=0.25,
        purchase_rate=0.70,
    ),
]


def generate_session(
    rng: random.Random,
    session_id: str,
    product_id: str,
    category: str,
    price: Decimal,
    start: datetime,
    cart_rate: float,
    purchase_rate: float,
) -> list[Event]:
    """Simulate one shopper visit: view, then maybe cart, then maybe purchase."""

    def make(event_type: EventType, minutes_later: int) -> Event:
        return Event(
            event_time=start + timedelta(minutes=minutes_later),
            event_type=event_type,
            session_id=session_id,
            user_id=f"user-{session_id}",
            product_id=product_id,
            category=category,
            price=price,
        )

    events = [make(EventType.VIEW, 0)]
    if rng.random() < cart_rate:
        events.append(make(EventType.CART, 2))
        if rng.random() < purchase_rate:
            events.append(make(EventType.PURCHASE, 5))
    return events


def generate_shop(
    products: list[ProductSpec],
    sessions_per_product: int,
    start: datetime,
    seed: int = 0,
) -> list[Event]:
    """Simulate many shopper visits across several products."""
    rng = random.Random(seed)
    events: list[Event] = []
    for product in products:
        for i in range(sessions_per_product):
            events.extend(
                generate_session(
                    rng=rng,
                    session_id=f"{product.product_id}-s{i}",
                    product_id=product.product_id,
                    category=product.category,
                    price=product.price,
                    start=start + timedelta(minutes=i * 10),
                    cart_rate=product.cart_rate,
                    purchase_rate=product.purchase_rate,
                )
            )
    return events
