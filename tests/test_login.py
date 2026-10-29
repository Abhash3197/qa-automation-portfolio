import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from config.settings import VALID_USER, VALID_PASSWORD, LOCKED_USER


@pytest.mark.smoke
def test_successful_login(page, base_url):
    """Verify successful login with valid credentials"""
    login_page = LoginPage(page, base_url)
    login_page.login(VALID_USER, VALID_PASSWORD)

    products_page = ProductsPage(page, base_url)
    assert products_page.get_product_count() > 0, "Products should be visible after login"


@pytest.mark.smoke
def test_login_with_invalid_credentials(page, base_url):
    """Verify login fails with invalid credentials"""
    login_page = LoginPage(page, base_url)
    login_page.login("invalid_user", "invalid_password")

    assert login_page.is_error_displayed(), "Error message should be shown"
    error_text = login_page.get_error_message()
    assert "user" in error_text.lower() or "invalid" in error_text.lower()


@pytest.mark.smoke
def test_locked_out_user_login(page, base_url):
    """Verify locked out user cannot login"""
    login_page = LoginPage(page, base_url)
    login_page.login(LOCKED_USER, VALID_PASSWORD)

    assert login_page.is_error_displayed(), "Error message should be shown for locked user"
    error_text = login_page.get_error_message()
    assert "locked" in error_text.lower()
