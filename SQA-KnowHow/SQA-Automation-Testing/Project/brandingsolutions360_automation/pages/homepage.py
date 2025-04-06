from pages.base_page import BasePage
from locators.homepage_locators import HomePageLocators

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def go_to_contact(self):
        self.click(HomePageLocators.CONTACT_BUTTON)

    def get_main_heading(self):
        return self.get_text(HomePageLocators.HEADER_TITLE)
