"""Turn metrics into findings: specific problems worth money."""

from dataclasses import dataclass
from decimal import Decimal

from cartpilot.metrics import CategoryFunnel

CART_ABANDONMENT = "cart_abandonment"


@dataclass(frozen=True)
class Finding:
    """One problem found in the shop's data."""

    rule: str
    subject: str
    observed: float
    baseline: float
    money_at_risk: Decimal
    severity: str


def shop_purchase_rate(funnels: list[CategoryFunnel]) -> float:
    """Share of all carts in the shop that became purchases."""
    carts = sum(f.carts for f in funnels)
    purchases = sum(f.purchases for f in funnels)
    return purchases / carts if carts else 0.0


def find_cart_abandonment(
    funnels: list[CategoryFunnel],
    min_carts: int = 30,
    weak_ratio: float = 0.6,
) -> list[Finding]:
    """Flag categories whose carts turn into purchases far less often than the shop."""
    baseline = shop_purchase_rate(funnels)
    findings = []
    for funnel in funnels:
        if funnel.carts < min_carts:
            continue
        if funnel.purchase_rate >= baseline * weak_ratio:
            continue
        severity = "high" if funnel.purchase_rate < baseline * 0.4 else "medium"
        findings.append(
            Finding(
                rule=CART_ABANDONMENT,
                subject=funnel.category,
                observed=funnel.purchase_rate,
                baseline=baseline,
                money_at_risk=funnel.abandoned_value,
                severity=severity,
            )
        )
    return sorted(findings, key=lambda f: f.money_at_risk, reverse=True)
