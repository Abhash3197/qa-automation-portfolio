import re

import pytest
from playwright.sync_api import expect

from config.settings import LOCKED_USER, VALID_PASSWORD, VALID_USER


@pytest.mark.smoke
def test_successful_login(login_page, products_page, page):
    login_page.login(VALID_USER, VALID_PASSWORD)

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(products_page.items).to_have_count(6)


@pytest.mark.smoke
def test_login_with_invalid_credentials(login_page):
    login_page.login("invalid_user", "invalid_password")

    expect(login_page.error).to_contain_text("do not match any user")


@pytest.mark.smoke
def test_locked_out_user_cannot_login(login_page):
    login_page.login(LOCKED_USER, VALID_PASSWORD)

    expect(login_page.error).to_contain_text("locked out")


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, message",
    [
        ("", VALID_PASSWORD, "Username is required"),
        (VALID_USER, "", "Password is required"),
    ],
)
def test_login_required_fields(login_page, username, password, message):
    login_page.login(username, password)

    expect(login_page.error).to_contain_text(message)


@pytest.mark.regression
def test_logout_returns_to_login(logged_in, page):
    page.locator("#react-burger-menu-btn").click()
    page.locator("[data-test='logout-sidebar-link']").click()

    expect(page).to_have_url("https://www.saucedemo.com/")


@pytest.mark.regression
def test_protected_page_requires_login(page, base_url):
    page.goto(f"{base_url}/inventory.html")

    expect(page.locator("[data-test='error']")).to_contain_text("only access '/inventory.html' when you are logged in")
