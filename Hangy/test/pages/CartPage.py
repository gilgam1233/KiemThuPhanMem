import time

from selenium.webdriver import Keys

from Hangy.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class CartPage(BasePage):
    URL = 'http://127.0.0.1:5000/cart'

    CART_NUMBER = (By.CLASS_NAME, 'cart-number')

    FIRST_PRODUCT = By.ID, 'cart1'
    NAME_PRODUCT = By.CSS_SELECTOR, '#cart1 > td:nth-child(2)'
    QUANTITY_PRODUCT = By.CSS_SELECTOR, '#cart1 > td:nth-child(4) > input'
    AMOUNT_PRODUCT = By.ID, 'item-total-1'
    DELETE_PRODUCT = By.CSS_SELECTOR, '#cart1 > td.text-center > button'


    NAME_ALL_PRODUCTS = By.CSS_SELECTOR, '.table tr > td:nth-child(2)'

    TOTAL_AMOUNT = By.ID, 'total-amount'
    VOUCHER_DISCOUNT = By.ID, 'voucher-discount'
    FINAL_AMOUNT = By.ID, 'final-amount'

    VOUCHER_SELECT = By.ID, 'voucher-select'
    PAY_BUTTON = By.CLASS_NAME, 'btn-pay'

    ALERT_DELETE = By.CLASS_NAME, 'swal2-icon-warning'
    ALERT_DELETE_CONFIRM = By.CLASS_NAME, 'swal2-confirm'
    ALERT_DELETE_CANCEL = By.CLASS_NAME, 'swal2-cancel'

    ALERT_EMPTY_CART = By.CLASS_NAME, 'alert'

    def open_page(self):
        self.open(self.URL)

    def get_first_cart_item(self):
        return self.find(*self.FIRST_PRODUCT)

    def get_cart_number(self):
        value = self.find(*self.CART_NUMBER)

        quantity = value.text

        if quantity == "":
            return 0

        return int(quantity)

    def get_name_all_products(self):
        return self.finds(*self.NAME_ALL_PRODUCTS)

    def get_name_product(self):
        return self.find(*self.NAME_PRODUCT)

    def get_quantity_product(self):
        return self.find(*self.QUANTITY_PRODUCT)

    def get_amount_product(self):
        return self.find(*self.AMOUNT_PRODUCT)

    def get_total_amount(self):
        return self.find(*self.TOTAL_AMOUNT)

    def get_voucher_discount(self):
        return self.find(*self.VOUCHER_DISCOUNT)

    def get_final_amount(self):
        return self.find(*self.FINAL_AMOUNT)

    def get_alert_empty_cart(self):
        return self.find(*self.ALERT_EMPTY_CART)

    def get_voucher_select(self):
        return self.find(*self.VOUCHER_SELECT)

    def update_quantity(self, kw):
        self.typing(*self.QUANTITY_PRODUCT,kw)

    def delete_product(self):
        self.find(*self.DELETE_PRODUCT).click()

    def confirm_delete_cart(self):
        self.find(*self.ALERT_DELETE_CONFIRM).click()

    def cancel_delete_cart(self):
        self.find(*self.ALERT_DELETE_CANCEL).click()

    def pay(self):
        self.find(*self.PAY_BUTTON).click()