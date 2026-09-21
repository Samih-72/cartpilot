"""Generate fake shop events with known, planted problems (for testing)."""

import random
from datetime import datetime, timedelta
from decimal import Decimal

from cartpilot.models import Event, EventType


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
