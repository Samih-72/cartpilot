# CartPilot AI

![CI](https://github.com/Samih-72/cartpilot/actions/workflows/ci.yml/badge.svg)

**AI-powered e-commerce conversion intelligence.**

CartPilot reads a shop's event data (product views, add-to-carts, purchases),
finds where revenue is being lost, and reports what to fix first.

> 🚧 **Status:** v0.1 in progress. The analysis pipeline and report work today;
> AI-written recommendations are next.

## Try it

Requirements: Python 3.12+ and [uv](https://docs.astral.sh/uv/)

```bash
git clone https://github.com/Samih-72/cartpilot.git
cd cartpilot
uv sync

# create a sample shop (synthetic data with a planted problem)
uv run python scripts/make_sample_csv.py

# analyse it
uv run cartpilot analyze data/sample_events.csv
```

This writes `report.md`. See [examples/sample-report.md](examples/sample-report.md)
for what it looks like:

```
1. **phones** - cart_abandonment (high severity)
   - Only **13%** of carts are purchased, against a shop average of 40%.
   - About **Rs 5,280,000** is sitting in abandoned carts.
```

## How it works

```
CSV -> validate -> DuckDB -> metrics (SQL) -> diagnostics -> report
```

| Stage | What it does |
|---|---|
| **Validate** | Every row is checked against a Pydantic schema. Bad rows are set aside with the line number and reason, never silently dropped or crashed on. |
| **Store** | Valid events are bulk-loaded into an in-process DuckDB database. |
| **Metrics** | Funnel, conversion rates, revenue and abandoned-cart value are computed in SQL. |
| **Diagnostics** | Rules compare each category to the shop's own baseline and estimate the money at risk. |
| **Report** | Findings first, ranked by money, then the funnel table and a data-quality summary. |

Design principle: **every number is computed by code**. The AI layer (coming in
v0.1) only explains and prioritises those numbers, so results stay reproducible
and testable.

## Development

```bash
uv run ruff format .
uv run ruff check .
uv run pytest
```

Test data is synthetic, generated with known planted problems (for example,
90% cart abandonment on phones), so the diagnostics can be tested against a
known ground truth.

## Roadmap

- [x] M0: Project skeleton (packaging, tests, linting, CI)
- [x] M1: Event schema + synthetic data generator
- [x] M2: CSV ingestion with validation + DuckDB loading
- [x] M3: Funnel and revenue metrics in SQL
- [x] M4: Diagnostics engine (cart abandonment rule)
- [x] M5: `cartpilot analyze` CLI + Markdown report
- [ ] M6: AI-written recommendations
- [ ] M7: Evaluation + v0.1.0 release

## License

MIT, see [LICENSE](LICENSE).
