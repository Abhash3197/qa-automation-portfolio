import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.settings import VALID_USER, VALID_PASSWORD


@pytest.fixture
def logged_in_with_items(page, base_url):
    """Fixture to login and add products to cart"""
    login_page = LoginPage(page, base_url)
    login_page.login(VALID_USER, VALID_PASSWORD)

    products_page = ProductsPage(page, base_url)
    products_page.add_product_to_cart("Sauce Labs Backpack")
    products_page.add_product_to_cart("Sauce Labs Bike Light")

    return page


@pytest.mark.regression
def test_complete_checkout_flow(logged_in_with_items, base_url):
    """Verify complete checkout flow from cart to order confirmation"""
    products_page = ProductsPage(logged_in_with_items, base_url)
    cart_page = CartPage(logged_in_with_items, base_url)
    checkout_page = CheckoutPage(logged_in_with_items, base_url)

    products_page.click_cart()
    assert cart_page.get_cart_items_count() == 2

    cart_page.proceed_to_checkout()
    checkout_page.fill_checkout_info("John", "Doe", "12345")
    checkout_page.continue_to_checkout_step_two()

    checkout_page.finish_order()
    assert checkout_page.is_order_confirmed(), "Order should be confirmed"


@pytest.mark.smoke
def test_checkout_missing_first_name(logged_in_with_items, base_url):
    """Verify checkout fails when first name is missing"""
    products_page = ProductsPage(logged_in_with_items, base_url)
    cart_page = CartPage(logged_in_with_items, base_url)
    checkout_page = CheckoutPage(logged_in_with_items, base_url)

    products_page.click_cart()
    cart_page.proceed_to_checkout()

    checkout_page.fill_checkout_info("", "Doe", "12345")
    checkout_page.continue_to_checkout_step_two()

    error = checkout_page.get_error_message()
    assert "first name" in error.lower(), "Error should mention first name"


@pytest.mark.regression
def test_checkout_missing_postal_code(logged_in_with_items, base_url):
    """Verify checkout fails when postal code is missing"""
    products_page = ProductsPage(logged_in_with_items, base_url)
    cart_page = CartPage(logged_in_with_items, base_url)
    checkout_page = CheckoutPage(logged_in_with_items, base_url)

    products_page.click_cart()
    cart_page.proceed_to_checkout()

    checkout_page.fill_checkout_info("John", "Doe", "")
    checkout_page.continue_to_checkout_step_two()

    error = checkout_page.get_error_message()
    assert "postal" in error.lower(), "Error should mention postal code"
