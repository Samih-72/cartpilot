"""First taste of DuckDB: the shop funnel in one SQL query."""

import duckdb

QUERY = """
SELECT
    category,
    COUNT(*) FILTER (WHERE event_type = 'view')     AS views,
    COUNT(*) FILTER (WHERE event_type = 'cart')     AS carts,
    COUNT(*) FILTER (WHERE event_type = 'purchase') AS buys,
    ROUND(buys / carts * 100, 1)                    AS cart_to_buy_pct
FROM 'data/sample_events.csv'
GROUP BY category
ORDER BY cart_to_buy_pct
"""

duckdb.sql(QUERY).show()
