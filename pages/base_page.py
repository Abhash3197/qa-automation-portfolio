from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = ""):
        self.page.goto(self.base_url + path)

    def by_test_id(self, value: str) -> Locator:
        """saucedemo exposes stable `data-test` attributes."""
        return self.page.locator(f"[data-test='{value}']")
