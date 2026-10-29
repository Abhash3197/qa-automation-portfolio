import pytest
from playwright.sync_api import sync_playwright
from config.settings import BASE_URL, HEADLESS, BROWSER_TYPE


@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = getattr(p, BROWSER_TYPE).launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def base_url():
    return BASE_URL
