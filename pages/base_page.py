from playwright.sync_api import Page
from config.settings import TIMEOUT


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.timeout = TIMEOUT

    def navigate(self, path: str = ""):
        url = self.base_url + path
        self.page.goto(url)

    def click(self, selector: str):
        self.page.click(selector, timeout=self.timeout)

    def fill(self, selector: str, text: str):
        self.page.fill(selector, text, timeout=self.timeout)

    def wait_for_element(self, selector: str):
        self.page.wait_for_selector(selector, timeout=self.timeout)

    def is_visible(self, selector: str) -> bool:
        try:
            self.page.wait_for_selector(selector, timeout=3000, state="visible")
            return True
        except Exception:
            return False

    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector)

    def get_all_texts(self, selector: str) -> list:
        return self.page.query_selector_all(selector)
