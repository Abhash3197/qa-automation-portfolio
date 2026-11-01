from pages.base_page import BasePage


class LoginPage(BasePage):
    def open(self):
        self.navigate()

    def login(self, username: str, password: str):
        self.open()
        self.by_test_id("username").fill(username)
        self.by_test_id("password").fill(password)
        self.by_test_id("login-button").click()

    @property
    def error(self):
        return self.by_test_id("error")
