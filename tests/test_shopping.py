import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from config.settings import VALID_USER, VALID_PASSWORD


@pytest.fixture
def logged_in_user(page, base_url):
    """Fixture to login before each test"""
    login_page = LoginPage(page, base_url)
    login_page.login(VALID_USER, VALID_PASSWORD)
    return page


@pytest.mark.smoke
def test_add_product_to_cart(logged_in_user, base_url):
    """Verify adding product to cart"""
    products_page = ProductsPage(logged_in_user, base_url)
    initial_count = products_page.get_cart_item_count()

    products_page.add_product_to_cart("Sauce Labs Backpack")
    updated_count = products_page.get_cart_item_count()

    assert updated_count == initial_count + 1, "Cart count should increase by 1"


@pytest.mark.smoke
def test_add_multiple_products(logged_in_user, base_url):
    """Verify adding multiple products to cart"""
    products_page = ProductsPage(logged_in_user, base_url)

    products_page.add_product_to_cart("Sauce Labs Backpack")
    products_page.add_product_to_cart("Sauce Labs Bike Light")

    assert products_page.get_cart_item_count() == 2, "Cart should have 2 items"


@pytest.mark.regression
def test_remove_product_from_cart(logged_in_user, base_url):
    """Verify removing product from cart"""
    products_page = ProductsPage(logged_in_user, base_url)
    cart_page = CartPage(logged_in_user, base_url)

    products_page.add_product_to_cart("Sauce Labs Backpack")
    products_page.click_cart()

    assert cart_page.get_cart_items_count() == 1
    cart_page.remove_item_from_cart("Sauce Labs Backpack")
    assert cart_page.get_cart_items_count() == 0


@pytest.mark.regression
def test_continue_shopping(logged_in_user, base_url):
    """Verify continue shopping button returns to products page"""
    products_page = ProductsPage(logged_in_user, base_url)
    cart_page = CartPage(logged_in_user, base_url)

    products_page.add_product_to_cart("Sauce Labs Backpack")
    products_page.click_cart()
    cart_page.continue_shopping()

    assert products_page.get_product_count() > 0, "Should be back on products page"
