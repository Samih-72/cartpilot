"""Create a sample CSV file from the pretend shop."""

from datetime import datetime
from pathlib import Path

from cartpilot.csv_files import write_events_csv
from cartpilot.synthetic import DEFAULT_PRODUCTS, generate_shop

path = Path("data/sample_events.csv")
path.parent.mkdir(exist_ok=True)

events = generate_shop(
    DEFAULT_PRODUCTS, sessions_per_product=1000, start=datetime(2026, 9, 1)
)
write_events_csv(events, path)
print(f"Saved {len(events)} events to {path}")
