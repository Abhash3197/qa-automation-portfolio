# UI Automation Portfolio — Sauce Demo

![UI Tests](https://github.com/Abhash3197/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)

UI test suite using **Playwright (Python)**, **pytest** and the **Page Object Model**, written against the public [Sauce Demo](https://www.saucedemo.com) shop.

## Results

18 tests (9 smoke, 9 regression) passed on three consecutive local runs. The full suite takes about 8 seconds with `-n 4` on Chromium.

| Area | Tests | Covers |
|---|---|---|
| Login | 7 | valid login, bad credentials, locked-out user, required-field errors, logout, protected-route redirect |
| Shopping | 7 | add / remove items, cart contents, continue shopping, sort by price and name |
| Checkout | 4 | full purchase with total-price check, required-field validation (first name, last name, postal code) |

## Quick start

```bash
git clone https://github.com/Abhash3197/qa-automation-portfolio.git
cd qa-automation-portfolio
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

pytest tests/ -m smoke        # critical journeys
pytest tests/ -n auto         # everything, in parallel
HEADLESS=false pytest tests/test_login.py -s   # watch it run
```

HTML report: add `--html=reports/report.html --self-contained-html`. Failed tests save a screenshot to `reports/`.

## Structure

```
pages/     page objects (login, products, cart, checkout) on a small BasePage
tests/     conftest fixtures + test modules, one per user journey
config/    base URL, browser, timeouts, known test users (env-overridable)
```

## Design decisions

- **Locators and `expect()` instead of raw element queries.** My first version used `query_selector_all` plus `networkidle` waits. It was slow and flaky: an assertion could run before the page had navigated, and the cart count came back 0 intermittently. Switching to `locator()` and `expect()` removed the flakiness and the manual waits.
- **One browser per worker, a fresh context per test.** Tests stay isolated without paying browser start-up on every test. This took the suite from about 130s to about 8s.
- **Stable `data-test` selectors.** The app exposes them, so tests don't depend on CSS classes.
- **Assertions check the user-visible outcome.** The purchase test checks the item total and tax-inclusive total, not just that a page loaded.
- **Page objects hold interactions. Tests hold assertions.**

## Flaky-test approach

1. Use auto-waiting `expect()` assertions and `wait_for_url` only after navigation clicks. Never use `sleep` or `networkidle`.
2. Each test logs in on its own, so tests share no state and are safe to run in parallel.
3. On failure the test saves a screenshot, and CI uploads it with the HTML report.
4. If a test is flaky, quarantine it with a marker and open an issue. Don't add retries to hide it.

## Limitations

- Only Chromium runs in CI. Firefox and WebKit would be a matrix addition.
- The app's `problem_user` and `performance_glitch_user` accounts aren't covered yet.
- There are no visual-regression or accessibility checks.
- Sauce Demo is a public site. A rare outage or change on its side can fail the suite.

## CI

GitHub Actions runs the full suite in parallel on every push and PR, and it uploads the HTML report and failure screenshots as an artifact.
