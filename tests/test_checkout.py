import re

import pytest
from playwright.sync_api import expect

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.fixture
def at_checkout(logged_in, cart_page):
    """Two items in the cart, on checkout step one."""
    logged_in.add_to_cart(BACKPACK)
    logged_in.add_to_cart(BIKE_LIGHT)
    logged_in.open_cart()
    cart_page.checkout()


@pytest.mark.smoke
def test_complete_purchase(at_checkout, checkout_page, page):
    checkout_page.fill_info("John", "Doe", "12345")
    checkout_page.continue_()

    # 29.99 + 9.99 items + 8% tax
    expect(checkout_page.by_test_id("subtotal-label")).to_have_text("Item total: $39.98")
    expect(checkout_page.summary_total).to_have_text("Total: $43.18")

    checkout_page.finish()

    expect(page).to_have_url(re.compile(r"/checkout-complete\.html$"))
    expect(checkout_page.confirmation_header).to_have_text("Thank you for your order!")


@pytest.mark.smoke
@pytest.mark.parametrize(
    "first, last, postal, message",
    [
        ("", "Doe", "12345", "First Name is required"),
        ("John", "", "12345", "Last Name is required"),
        ("John", "Doe", "", "Postal Code is required"),
    ],
)
def test_checkout_required_fields(at_checkout, checkout_page, first, last, postal, message):
    checkout_page.fill_info(first, last, postal)
    checkout_page.continue_()

    expect(checkout_page.error).to_contain_text(message)
