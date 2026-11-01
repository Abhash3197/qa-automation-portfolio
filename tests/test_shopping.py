import pytest
from playwright.sync_api import expect

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
def test_add_product_to_cart(logged_in):
    logged_in.add_to_cart(BACKPACK)

    expect(logged_in.cart_badge).to_have_text("1")


@pytest.mark.smoke
def test_add_multiple_products(logged_in):
    logged_in.add_to_cart(BACKPACK)
    logged_in.add_to_cart(BIKE_LIGHT)

    expect(logged_in.cart_badge).to_have_text("2")


@pytest.mark.regression
def test_cart_lists_added_products(logged_in, cart_page):
    logged_in.add_to_cart(BACKPACK)
    logged_in.add_to_cart(BIKE_LIGHT)
    logged_in.open_cart()

    expect(cart_page.items).to_have_count(2)
    assert sorted(cart_page.item_names()) == sorted([BACKPACK, BIKE_LIGHT])


@pytest.mark.regression
def test_remove_product_from_cart(logged_in, cart_page):
    logged_in.add_to_cart(BACKPACK)
    logged_in.open_cart()
    expect(cart_page.items).to_have_count(1)

    cart_page.remove(BACKPACK)

    expect(cart_page.items).to_have_count(0)


@pytest.mark.regression
def test_continue_shopping_returns_to_inventory(logged_in, cart_page):
    logged_in.add_to_cart(BACKPACK)
    logged_in.open_cart()

    cart_page.continue_shopping()

    expect(logged_in.items).to_have_count(6)


@pytest.mark.regression
def test_sort_price_low_to_high(logged_in):
    logged_in.sort_by("lohi")

    prices = logged_in.prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_sort_name_z_to_a(logged_in):
    logged_in.sort_by("za")

    names = logged_in.names()
    assert names == sorted(names, reverse=True)
