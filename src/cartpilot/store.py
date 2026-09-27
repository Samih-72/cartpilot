"""Put validated events into an in-memory DuckDB database."""

import duckdb

from cartpilot.models import Event

CREATE_TABLE = """
CREATE TABLE events (
    event_time TIMESTAMP,
    event_type VARCHAR,
    session_id VARCHAR,
    user_id    VARCHAR,
    product_id VARCHAR,
    category   VARCHAR,
    brand      VARCHAR,
    price      DECIMAL(12, 2)
)
"""

INSERT_ROW = "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)"


def load_events(events: list[Event]) -> duckdb.DuckDBPyConnection:
    """Create an in-memory database holding these validated events."""
    con = duckdb.connect()
    con.execute(CREATE_TABLE)
    rows = [
        (
            event.event_time,
            event.event_type.value,
            event.session_id,
            event.user_id,
            event.product_id,
            event.category,
            event.brand,
            event.price,
        )
        for event in events
    ]
    # One transaction for the whole batch: far faster than committing each row.
    con.execute("BEGIN TRANSACTION")
    con.executemany(INSERT_ROW, rows)
    con.execute("COMMIT")
    return con
