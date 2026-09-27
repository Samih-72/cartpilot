"""Command line interface: cartpilot analyze <file>."""

import argparse
from pathlib import Path

from cartpilot.csv_files import read_events_csv
from cartpilot.diagnostics import find_cart_abandonment
from cartpilot.metrics import funnel_by_category
from cartpilot.report import render_report
from cartpilot.store import load_events

DEFAULT_OUTPUT = Path("report.md")


def analyze(path: Path) -> str:
    """Run the whole pipeline on one CSV file and return the report text."""
    events, bad_rows = read_events_csv(path)
    funnels = funnel_by_category(load_events(events))
    findings = find_cart_abandonment(funnels)
    return render_report(
        source=path,
        event_count=len(events),
        bad_rows=bad_rows,
        funnels=funnels,
        findings=findings,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cartpilot",
        description="Find what is losing an online shop money.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    analyze_command = commands.add_parser("analyze", help="analyse a shop event CSV")
    analyze_command.add_argument("path", type=Path, help="CSV file of shop events")
    analyze_command.add_argument(
        "-o",
        "--out",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"where to write the report (default: {DEFAULT_OUTPUT})",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.path.exists():
        print(f"File not found: {args.path}")
        return 1

    report = analyze(args.path)
    args.out.write_text(report, encoding="utf-8")
    print(report)
    print(f"Report saved to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
