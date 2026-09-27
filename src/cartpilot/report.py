"""Turn metrics and findings into a readable Markdown report."""

from datetime import datetime
from pathlib import Path

from cartpilot.csv_files import BadRow
from cartpilot.diagnostics import Finding
from cartpilot.metrics import CategoryFunnel

MAX_BAD_ROWS_SHOWN = 10


def _findings_section(findings: list[Finding]) -> list[str]:
    if not findings:
        return [
            "No major problems found. Every category converts close to the "
            "shop average."
        ]

    lines = []
    for number, finding in enumerate(findings, start=1):
        lines.append(
            f"{number}. **{finding.subject}** — {finding.rule} "
            f"({finding.severity} severity)"
        )
        lines.append(
            f"   - Only **{finding.observed:.0%}** of carts are purchased, "
            f"against a shop average of {finding.baseline:.0%}."
        )
        lines.append(
            f"   - About **Rs {finding.money_at_risk:,.0f}** is sitting in "
            f"abandoned carts."
        )
    return lines


def _funnel_table(funnels: list[CategoryFunnel]) -> list[str]:
    lines = [
        "| Category | Views | Carts | Purchases | Cart rate | Purchase rate "
        "| Revenue | In abandoned carts |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for f in funnels:
        lines.append(
            f"| {f.category} | {f.views:,} | {f.carts:,} | {f.purchases:,} "
            f"| {f.cart_rate:.0%} | {f.purchase_rate:.0%} "
            f"| Rs {f.revenue:,.0f} | Rs {f.abandoned_value:,.0f} |"
        )
    return lines


def _data_quality_section(event_count: int, bad_rows: list[BadRow]) -> list[str]:
    lines = [
        f"- Rows accepted: **{event_count:,}**",
        f"- Rows rejected: **{len(bad_rows)}**",
    ]
    for bad in bad_rows[:MAX_BAD_ROWS_SHOWN]:
        lines.append(f"  - line {bad.line_number}: {bad.reason}")
    if len(bad_rows) > MAX_BAD_ROWS_SHOWN:
        lines.append(f"  - ...and {len(bad_rows) - MAX_BAD_ROWS_SHOWN} more")
    return lines


def render_report(
    source: Path,
    event_count: int,
    bad_rows: list[BadRow],
    funnels: list[CategoryFunnel],
    findings: list[Finding],
    now: datetime | None = None,
) -> str:
    """Build the full Markdown report as one string."""
    generated = (now or datetime.now()).strftime("%Y-%m-%d %H:%M")
    lines = [
        "# CartPilot report",
        "",
        f"Source file: `{source}`  ",
        f"Generated: {generated}",
        "",
        "## What is costing you money",
        "",
        *_findings_section(findings),
        "",
        "## Funnel by category",
        "",
        *_funnel_table(funnels),
        "",
        "## Data quality",
        "",
        *_data_quality_section(event_count, bad_rows),
        "",
    ]
    return "\n".join(lines)
