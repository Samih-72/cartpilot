"""Shop metrics, computed with SQL."""

from dataclasses import dataclass
from decimal import Decimal

import duckdb

FUNNEL_BY_CATEGORY = """
SELECT
    COALESCE(category, 'unknown') AS category,
    COUNT(*) FILTER (WHERE event_type = 'view')     AS views,
    COUNT(*) FILTER (WHERE event_type = 'cart')     AS carts,
    COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchases,
    COALESCE(SUM(price) FILTER (WHERE event_type = 'purchase'), 0) AS revenue,
    COALESCE(SUM(price) FILTER (WHERE event_type = 'cart'), 0)
        - COALESCE(SUM(price) FILTER (WHERE event_type = 'purchase'), 0)
        AS abandoned_value
FROM events
GROUP BY 1
ORDER BY abandoned_value DESC
"""


@dataclass(frozen=True)
class CategoryFunnel:
    """Funnel numbers for one product category."""

    category: str
    views: int
    carts: int
    purchases: int
    revenue: Decimal
    abandoned_value: Decimal

    @property
    def cart_rate(self) -> float:
        """Share of viewers who added to cart."""
        return self.carts / self.views if self.views else 0.0

    @property
    def purchase_rate(self) -> float:
        """Share of carts that became purchases."""
        return self.purchases / self.carts if self.carts else 0.0


def funnel_by_category(con: duckdb.DuckDBPyConnection) -> list[CategoryFunnel]:
    """Return funnel numbers for each category, worst abandonment first."""
    rows = con.execute(FUNNEL_BY_CATEGORY).fetchall()
    return [CategoryFunnel(*row) for row in rows]
