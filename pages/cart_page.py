from pages.base_page import BasePage


class CartPage(BasePage):
    # Selectors
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    REMOVE_BUTTON = "[data-test*='remove']"
    CART_QUANTITY = ".cart_quantity"

    def navigate_to_cart(self):
        self.navigate("/cart.html")

    def get_cart_items_count(self) -> int:
        items = self.page.query_selector_all(self.CART_ITEM)
        return len(items)

    def remove_item_from_cart(self, product_name: str):
        items = self.page.query_selector_all(self.CART_ITEM)
        for item in items:
            name = item.query_selector(self.CART_ITEM_NAME).text_content()
            if product_name.lower() in name.lower():
                item.query_selector(self.REMOVE_BUTTON).click()
                return

    def get_cart_item_names(self) -> list:
        items = self.page.query_selector_all(self.CART_ITEM)
        return [item.query_selector(self.CART_ITEM_NAME).text_content() for item in items]

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
