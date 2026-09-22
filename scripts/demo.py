"""Quick demo: find the leaky product in a shop's CSV file."""

import sys
from collections import Counter
from pathlib import Path

from cartpilot.csv_files import read_events_csv
from cartpilot.models import EventType

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/sample_events.csv")
events, bad_rows = read_events_csv(path)

print(f"Read {len(events)} good rows from {path}")
print(f"Set aside {len(bad_rows)} bad rows")
for bad in bad_rows[:5]:
    print(f"  line {bad.line_number}: {bad.reason}")
print()

counts = Counter((e.category or "unknown", e.event_type) for e in events)
prices = {e.category or "unknown": e.price for e in events}

print(f"{'Product':<10}{'Views':>7}{'Carts':>7}{'Buys':>7}", end="")
print(f"{'Cart->Buy':>11}{'Lost Rs':>12}")
for category in sorted(prices):
    views = counts[(category, EventType.VIEW)]
    carts = counts[(category, EventType.CART)]
    buys = counts[(category, EventType.PURCHASE)]
    rate = buys / carts if carts else 0
    lost = (carts - buys) * prices[category]
    flag = "  <-- PROBLEM" if rate < 0.3 else ""
    print(f"{category:<10}{views:>7}{carts:>7}{buys:>7}{rate:>11.0%}{lost:>12,}{flag}")
