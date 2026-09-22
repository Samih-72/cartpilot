"""Save shop events to CSV files."""

import csv
from pathlib import Path

from cartpilot.models import Event

COLUMNS = list(Event.model_fields)


def write_events_csv(events: list[Event], path: Path) -> None:
    """Save events to a CSV file, one row per event."""
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for event in events:
            writer.writerow(event.model_dump(mode="json"))
