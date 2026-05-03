from selenium.webdriver.common.by import By

from Hangy.test.pages.BasePage import BasePage


class OrderHistoryPage(BasePage):
    URL = 'http://127.0.0.1:5000/order_history'

    LIST_ORDERS = By.CSS_SELECTOR, 'body > div > table > tbody > tr > td:nth-child(1)'

    def open_page(self):
        self.driver.get(self.URL)

    def get_order_history(self):
        return self.finds(*self.LIST_ORDERS)