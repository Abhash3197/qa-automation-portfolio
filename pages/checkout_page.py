from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.by_test_id("firstName").fill(first_name)
        self.by_test_id("lastName").fill(last_name)
        self.by_test_id("postalCode").fill(postal_code)

    def continue_(self):
        self.by_test_id("continue").click()

    def finish(self):
        self.by_test_id("finish").click()

    @property
    def error(self):
        return self.by_test_id("error")

    @property
    def summary_total(self):
        return self.by_test_id("total-label")

    @property
    def confirmation_header(self):
        return self.by_test_id("complete-header")
