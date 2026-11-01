from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from config.settings import BASE_URL, BROWSER_TYPE, HEADLESS, TIMEOUT, VALID_PASSWORD, VALID_USER
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

REPORTS = Path("reports")


@pytest.fixture(scope="session")
def browser():
    """One browser per worker; each test still gets an isolated context."""
    with sync_playwright() as p:
        browser = getattr(p, BROWSER_TYPE).launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture
def page(browser, request):
    context = browser.new_context()
    context.set_default_timeout(TIMEOUT)
    page = context.new_page()
    yield page
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        REPORTS.mkdir(exist_ok=True)
        page.screenshot(path=str(REPORTS / f"{request.node.name}.png"))
    context.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"rep_{call.when}", outcome.get_result())


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def login_page(page, base_url):
    return LoginPage(page, base_url)


@pytest.fixture
def products_page(page, base_url):
    return ProductsPage(page, base_url)


@pytest.fixture
def cart_page(page, base_url):
    return CartPage(page, base_url)


@pytest.fixture
def checkout_page(page, base_url):
    return CheckoutPage(page, base_url)


@pytest.fixture
def logged_in(login_page, products_page):
    """Logged in as standard_user, on the inventory page."""
    login_page.login(VALID_USER, VALID_PASSWORD)
    return products_page
