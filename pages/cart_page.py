from pages.base_page import BasePage
from pages.products_page import slugify


class CartPage(BasePage):
    @property
    def items(self):
        return self.by_test_id("inventory-item")

    def item_names(self) -> list[str]:
        return self.by_test_id("inventory-item-name").all_text_contents()

    def remove(self, product_name: str):
        self.by_test_id(f"remove-{slugify(product_name)}").click()

    def continue_shopping(self):
        self.by_test_id("continue-shopping").click()
        self.page.wait_for_url("**/inventory.html")

    def checkout(self):
        self.by_test_id("checkout").click()
        self.page.wait_for_url("**/checkout-step-one.html")
