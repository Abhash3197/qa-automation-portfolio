from pages.base_page import BasePage


class ProductsPage(BasePage):
    # Selectors
    PRODUCTS_CONTAINER = ".inventory_list"
    PRODUCT_ITEM = ".inventory_list .inventory_item"
    PRODUCT_NAME = ".inventory_item_name"
    PRODUCT_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "button[data-test*='add-to-cart']"
    REMOVE_BUTTON = "button[data-test*='remove']"
    CART_BADGE = "[class*='cart_badge']"
    CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = ".product_sort_container"
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def add_product_to_cart(self, product_name: str):
        products = self.page.query_selector_all(self.PRODUCT_ITEM)
        for product in products:
            name = product.query_selector(self.PRODUCT_NAME).text_content()
            if product_name.lower() in name.lower():
                product.query_selector(self.ADD_TO_CART_BUTTON).click()
                return

    def get_product_count(self) -> int:
        products = self.page.query_selector_all(self.PRODUCT_ITEM)
        return len(products)

    def get_cart_item_count(self) -> int:
        try:
            return int(self.get_text(self.CART_BADGE).strip())
        except Exception:
            return 0

    def click_cart(self):
        self.click(self.CART_LINK)
        self.page.wait_for_load_state("networkidle")

    def sort_products(self, sort_option: str):
        self.click(self.SORT_DROPDOWN)
        self.page.select_option(self.SORT_DROPDOWN, sort_option)

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
