from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # Selectors - Step One
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    ERROR_MESSAGE = "[data-test='error']"

    # Step Two
    FINISH_BUTTON = "[data-test='finish']"
    TOTAL_PRICE = ".summary_total_label"

    # Confirmation
    THANK_YOU_MESSAGE = ".complete-header"
    ORDER_CONFIRMATION_TEXT = ".complete-text"

    def navigate_to_checkout(self):
        self.navigate("/checkout-step-one.html")

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)

    def continue_to_checkout_step_two(self):
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def finish_order(self):
        self.click(self.FINISH_BUTTON)

    def is_order_confirmed(self) -> bool:
        return self.is_visible(self.THANK_YOU_MESSAGE)

    def get_order_confirmation_text(self) -> str:
        return self.get_text(self.THANK_YOU_MESSAGE).strip()

    def get_total_price(self) -> str:
        return self.get_text(self.TOTAL_PRICE).strip()
