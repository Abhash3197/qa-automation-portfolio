from pages.base_page import BasePage


def slugify(product_name: str) -> str:
    return product_name.lower().replace(" ", "-")


class ProductsPage(BasePage):
    @property
    def items(self):
        return self.by_test_id("inventory-item")

    @property
    def cart_badge(self):
        return self.by_test_id("shopping-cart-badge")

    def add_to_cart(self, product_name: str):
        self.by_test_id(f"add-to-cart-{slugify(product_name)}").click()

    def remove_from_cart(self, product_name: str):
        self.by_test_id(f"remove-{slugify(product_name)}").click()

    def open_cart(self):
        self.by_test_id("shopping-cart-link").click()
        self.page.wait_for_url("**/cart.html")

    def sort_by(self, option_value: str):
        """option_value: az | za | lohi | hilo"""
        self.by_test_id("product-sort-container").select_option(option_value)

    def prices(self) -> list[float]:
        texts = self.by_test_id("inventory-item-price").all_text_contents()
        return [float(t.replace("$", "")) for t in texts]

    def names(self) -> list[str]:
        return self.by_test_id("inventory-item-name").all_text_contents()
