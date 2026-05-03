import time

from selenium.webdriver import Keys

from Hangy.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    URL = 'http://127.0.0.1:5000/'

    CART_BUTTON = (By.CLASS_NAME, 'btn-cart')
    CART_NUMBER = (By.CLASS_NAME, 'cart-number')
    ORDER_HISTORY_BUTTON = (By.CSS_SELECTOR, '#navbarSupportedContent > div:nth-child(3) > form > div.dropdown > ul > li:nth-child(2) > a')

    USER_DROPDOWN = (By.ID, 'dropdownUser1')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '#navbarSupportedContent > div:nth-child(3) > form > div.dropdown > ul > li:nth-child(4) > a')

    SEARCH_INPUT = (By.NAME, 'kw')
    SEARCH_BUTTON = (By.CLASS_NAME, 'btn-search')
    NAME_PRODUCT = (By.CSS_SELECTOR, 'body > div > div:nth-child(1) > div.info > h6')
    ADD_CART_BUTTON = (By.CSS_SELECTOR, 'body > div > div:nth-child(1) > div.btn-add-cart > button')
    ADD_CART_BUTTON_2 = (By.CSS_SELECTOR, 'body > div > div:nth-child(2) > div.btn-add-cart > button')
    LOGIN_BUTTON = (By.CLASS_NAME, 'btn-login')

    PAGE_BUTTON = (By.CSS_SELECTOR, 'body > nav > ul > li:nth-child(2)')

    def open_page(self):
        self.open(self.URL)

    def go_to_cart(self):
        self.click(*self.CART_BUTTON)

    def go_to_login(self):
        self.click(*self.LOGIN_BUTTON)

    def go_to_order_history(self):
        self.click(*self.ORDER_HISTORY_BUTTON)

    def logout(self):
        self.click(*self.USER_DROPDOWN)
        self.click(*self.LOGOUT_BUTTON)

    def search(self, kw):
        self.typing(*self.SEARCH_INPUT, kw + Keys.ENTER)

    def add_to_cart(self):
        self.click(*self.ADD_CART_BUTTON)

    def add_products_to_cart(self):
        self.click(*self.ADD_CART_BUTTON)
        time.sleep(1)
        self.click(*self.ADD_CART_BUTTON_2)

    def go_to_next_page(self):
        self.click(*self.PAGE_BUTTON)

    def get_cart_number(self):
        value = self.find(*self.CART_NUMBER)

        quantity = value.text

        if quantity == "":
            return 0

        return int(quantity)

    def get_name_product(self):
        return self.find(*self.NAME_PRODUCT)
