# QA Automation Portfolio - SauceLabs Demo App

A production-grade test automation suite demonstrating SDET best practices using **Playwright**, **Python**, and the **Page Object Model** pattern.

**Target**: [SauceLabs Demo App](https://www.saucedemo.com) — a public e-commerce application designed for testing.

## What This Tests

✅ **Authentication** — Valid/invalid login, account lockout  
✅ **Product Browsing** — Product visibility, catalog operations  
✅ **Shopping Cart** — Add/remove items, cart persistence  
✅ **Checkout Flow** — Multi-step form validation, order completion  

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation
```bash
git clone <repo>
cd qa-automation-portfolio
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

### Run Tests
```bash
# Smoke tests only (5 min)
pytest tests/ -m smoke -v

# Full suite (10 min)
pytest tests/ -v

# Parallel execution
pytest tests/ -v -n auto

# With HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html
```

## Project Structure

```
qa-automation-portfolio/
├── pages/                    # Page Object Model
│   ├── base_page.py        # Shared methods
│   ├── login_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                    # Test suites
│   ├── conftest.py         # Pytest fixtures
│   ├── test_login.py       # Authentication
│   ├── test_shopping.py    # Cart operations
│   └── test_checkout.py    # Checkout flow
├── config/
│   └── settings.py         # Environment config
├── requirements.txt
├── pytest.ini
└── .github/workflows/       # CI/CD
```

## Test Coverage

| Suite | Tests | Status | Purpose |
|-------|-------|--------|---------|
| **Login** | 3 | ✅ Smoke | Authentication, error handling |
| **Shopping** | 4 | ✅ Mixed | Cart operations, product browsing |
| **Checkout** | 3 | ✅ Mixed | Multi-step validation, order flow |
| **Total** | 10 | ✅ | End-to-end user journeys |

## Architecture Decisions

### 1. **Page Object Model (POM)**
- Each page is a class with selectors and methods
- Tests remain readable; maintenance is centralized
- Changes to UI selectors require updates in one place only

### 2. **Playwright + Python**
- **Why**: Lightweight, fast, multi-browser support (Chromium, Firefox, WebKit)
- **Why Python**: Simpler syntax, faster test development
- **Why not Selenium**: Playwright has built-in waits, no flaky sleeps

### 3. **Test Markers (smoke/regression)**
- `@pytest.mark.smoke`: 5 critical paths, runs in CI on every commit
- `@pytest.mark.regression`: Full suite, scheduled nightly
- Allows flexibility in CI/CD cadence

### 4. **HTML Reports**
- `pytest-html` generates self-contained reports
- Uploaded as GitHub Actions artifacts for zero-setup review
- Includes screenshots on failure (future enhancement)

## CI/CD Pipeline

- **Trigger**: Every push to `main` or `develop`, all PRs
- **Runs**: Smoke tests first (fast feedback), then full suite in parallel
- **Report**: HTML uploaded to GitHub Actions, linked in PR
- **Badge**: (TBD) Add passing/failing badge to README

## Known Limitations & Roadmap

- **No screenshots on failure** — Add `page.screenshot()` in conftest for next iteration
- **API tests** — Coming next; will test endpoints with pytest + requests
- **Visual regression** — Consider adding Playwright Test reporter or Percy
- **Data-driven tests** — Parameterize checkout form tests with @pytest.mark.parametrize

## Flaky Test Strategy

Currently stable (no flaky tests in baseline). If failures occur:

1. **Wait time issues**: Increase `TIMEOUT` in `config/settings.py`
2. **Race conditions**: Add `page.wait_for_load_state("networkidle")` before assertions
3. **Selector stability**: Prefer `data-test` attributes over class names

## Local Development

```bash
# Run with headed browser (watch execution)
HEADLESS=false pytest tests/test_login.py -v -s

# Run a single test
pytest tests/test_login.py::test_successful_login -v

# Debug with pdb
pytest tests/test_login.py -v --pdb
```

## Files Not Included (Why)

- `.env` — Each dev/CI uses local settings; no credentials stored
- `reports/` — Generated at runtime, gitignored
- `playwright/` — Browser binaries downloaded by `playwright install`

## Metrics & Results

**Latest Run** (as of last commit):
- Tests: 10/10 passing ✅
- Duration: ~45 seconds
- Flakes: 0
- Browser: Chromium on Linux

## Next Steps

1. **Parameterized checkout tests** — Test multiple user types (performance_glitch_user, problem_user)
2. **API test suite** — POST /auth, GET /products, POST /order
3. **Allure reporting** — Richer metrics, trend analysis
4. **Docker image** — Reproducible test environment
5. **Test data management** — Fixture factories for complex scenarios

## Contact

Questions or feedback? Open an issue or reach out to shreya.strategicdesign@gmail.com

---

**Built with**: Playwright 1.40 | Python 3.11 | pytest 7.4 | GitHub Actions
