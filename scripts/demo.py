"""Quick demo: find the leaky product in a fake shop."""

from datetime import datetime

from cartpilot.models import EventType
from cartpilot.synthetic import DEFAULT_PRODUCTS, generate_shop

events = generate_shop(
    DEFAULT_PRODUCTS, sessions_per_product=1000, start=datetime(2026, 9, 1)
)
print(f"Pretend shop created: {len(events)} shopper actions\n")

print(f"{'Product':<10}{'Views':>7}{'Carts':>7}{'Buys':>7}", end="")
print(f"{'Cart->Buy':>11}{'Lost Rs':>12}")
for product in DEFAULT_PRODUCTS:
    mine = [e for e in events if e.product_id == product.product_id]
    views = sum(e.event_type == EventType.VIEW for e in mine)
    carts = sum(e.event_type == EventType.CART for e in mine)
    buys = sum(e.event_type == EventType.PURCHASE for e in mine)
    rate = buys / carts
    lost = (carts - buys) * product.price
    flag = "  <-- PROBLEM" if rate < 0.3 else ""
    print(
        f"{product.category:<10}{views:>7}{carts:>7}{buys:>7}"
        f"{rate:>11.0%}{lost:>12,}{flag}"
    )
