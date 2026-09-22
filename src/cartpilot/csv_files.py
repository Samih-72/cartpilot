"""Save and load shop events as CSV files."""

import csv
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from cartpilot.models import Event

COLUMNS = list(Event.model_fields)


@dataclass(frozen=True)
class BadRow:
    """A row that broke the rules, and why."""

    line_number: int
    reason: str


def write_events_csv(events: list[Event], path: Path) -> None:
    """Save events to a CSV file, one row per event."""
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for event in events:
            writer.writerow(event.model_dump(mode="json"))


def read_events_csv(path: Path) -> tuple[list[Event], list[BadRow]]:
    """Load events from a CSV file. Keep good rows; list bad rows with reasons."""
    good: list[Event] = []
    bad: list[BadRow] = []
    with path.open(newline="", encoding="utf-8") as f:
        for line_number, row in enumerate(csv.DictReader(f), start=2):
            cleaned = {key: value or None for key, value in row.items()}
            try:
                good.append(Event(**cleaned))
            except ValidationError as error:
                first = error.errors()[0]
                reason = f"{first['loc'][0]}: {first['msg']}"
                bad.append(BadRow(line_number=line_number, reason=reason))
    return good, bad
