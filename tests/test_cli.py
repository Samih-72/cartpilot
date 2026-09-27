"""Tests for the command line tool."""

from datetime import datetime

from cartpilot.cli import analyze, main
from cartpilot.csv_files import write_events_csv
from cartpilot.synthetic import DEFAULT_PRODUCTS, generate_shop

HEADER = "event_time,event_type,session_id,user_id,product_id,category,brand,price"


def make_shop_csv(path):
    events = generate_shop(
        DEFAULT_PRODUCTS, sessions_per_product=200, start=datetime(2026, 9, 1)
    )
    write_events_csv(events, path)
    return path


def test_analyze_reports_the_phone_problem(tmp_path):
    csv_path = make_shop_csv(tmp_path / "events.csv")

    report = analyze(csv_path)

    assert "# CartPilot report" in report
    assert "phones" in report
    assert "cart_abandonment" in report
    assert "Rows rejected: **0**" in report


def test_main_writes_a_report_file(tmp_path, capsys):
    csv_path = make_shop_csv(tmp_path / "events.csv")
    out_path = tmp_path / "report.md"

    exit_code = main(["analyze", str(csv_path), "--out", str(out_path)])

    assert exit_code == 0
    assert out_path.exists()
    assert "Funnel by category" in out_path.read_text(encoding="utf-8")
    assert "Report saved to" in capsys.readouterr().out


def test_bad_rows_are_reported_but_do_not_stop_the_analysis(tmp_path):
    csv_path = tmp_path / "messy.csv"
    csv_path.write_text(
        "\n".join(
            [
                HEADER,
                "2026-09-01T10:00:00,view,s1,u1,p1,phones,,15000",
                "2026-09-01T10:01:00,banana,s2,u2,p1,phones,,15000",
            ]
        ),
        encoding="utf-8",
    )

    report = analyze(csv_path)

    assert "Rows accepted: **1**" in report
    assert "Rows rejected: **1**" in report
    assert "line 3: event_type" in report


def test_missing_file_returns_an_error_code(tmp_path, capsys):
    exit_code = main(["analyze", str(tmp_path / "nope.csv")])

    assert exit_code == 1
    assert "File not found" in capsys.readouterr().out
