import time

from selenium.webdriver import Keys

from Hangy.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class AdminOrderPage(BasePage):
    URL = 'http://127.0.0.1:5000/admin/order'

    CREATE_BUTTON = By.CSS_SELECTOR, '.container-body > ul.nav.nav-tabs > li:nth-child(2) > a'
    EDIT_BUTTON = By.CSS_SELECTOR, '.container-body > div > table > tbody > tr:last-child > td.list-buttons-column > a'
    DELETE_BUTTON = By.CSS_SELECTOR, '.container-body table tr:last-child > td.list-buttons-column > form > button'

    DATA_TOTAL_AMOUNT = By.ID, 'total_amount'
    DATA_FINAL_AMOUNT = By.ID, 'final_amount'
    DATA_USER_SELECT = By.CSS_SELECTOR, '#s2id_user span.select2-chosen'
    DATA_USER_INPUT = By.ID, 's2id_autogen4_search'
    DATA_STATUS_SELECT = By.CSS_SELECTOR, '#s2id_status .select2-chosen'
    DATA_STATUS_INPUT = By.ID, 's2id_autogen3_search'

    ALERT = By.CSS_SELECTOR, '.container-body .alert'
    PAGE = By.CSS_SELECTOR, 'body > div.container.flex-column > div.container-body > ul.pagination > li:nth-last-child(3) > a'

    SAVE_BUTTON = By.CSS_SELECTOR, 'body > div.container.flex-column > div.container-body > form > fieldset > div:nth-child(9) > div > input.btn.btn-primary'


    def open_page(self):
        self.open(self.URL)

    def go_to_create_page(self):
        self.click(*self.CREATE_BUTTON)

    def go_to_edit_page(self):
        self.click(*self.EDIT_BUTTON)

    def create_new_order(self, total, final, user):
        self.click(*self.DATA_USER_SELECT)
        self.typing(*self.DATA_USER_INPUT, user + Keys.ENTER)
        self.typing(*self.DATA_TOTAL_AMOUNT, total + Keys.ENTER)
        self.typing(*self.DATA_FINAL_AMOUNT, final + Keys.ENTER)

    def edit_status_order(self, kw):
        self.click(*self.DATA_STATUS_SELECT)
        self.typing(*self.DATA_STATUS_INPUT, kw + Keys.ENTER)

    def alert(self):
        return self.find(*self.ALERT)

    def delete_order(self):
        self.click(*self.DELETE_BUTTON)

    def save_order(self):
        self.click(*self.SAVE_BUTTON)

    def get_page(self):
        return self.find(*self.PAGE)

    def go_to_last_page(self):
        self.click(*self.PAGE)