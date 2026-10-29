from pages.base_page import BasePage


class LoginPage(BasePage):
    # Selectors
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def login(self, username: str, password: str):
        self.navigate()
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE).strip()

    def is_error_displayed(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
