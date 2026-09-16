# CartPilot AI

![CI](https://github.com/Samih-72/cartpilot/actions/workflows/ci.yml/badge.svg)

**AI-powered e-commerce conversion intelligence.**

CartPilot analyzes a store's event data (product views, add-to-carts, purchases),
finds where revenue is being lost, and recommends what to fix.

> 🚧 **Status:** early development (v0.1 in progress). Not ready for use yet.

## How it will work (v0.1)

```
CSV events → validate → metrics (SQL) → problem detection → AI recommendations → report
```

- All numbers are computed by code, so they are reproducible and testable.
- The AI only explains the findings and suggests actions.

## Development setup

Requirements: Python 3.12+, [uv](https://docs.astral.sh/uv/)

```bash
git clone https://github.com/Samih-72/cartpilot.git
cd cartpilot
uv sync
```

Run the checks:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

## Roadmap

- [x] M0: Project skeleton (packaging, tests, linting, CI)
- [ ] M1: Event schema + synthetic test data
- [ ] M2: Data ingestion + validation
- [ ] M3: Metrics layer
- [ ] M4: Diagnostics engine
- [ ] M5: Report generation
- [ ] M6: AI recommendations
- [ ] M7: Evaluation + v0.1.0 release

## License

MIT, see [LICENSE](LICENSE).