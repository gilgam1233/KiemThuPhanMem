import time

from selenium.webdriver import Keys

from Hangy.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class AdminUserVoucherPage(BasePage):
    URL = 'http://127.0.0.1:5000/admin/uservoucher'

    CREATE_BUTTON = By.CSS_SELECTOR, '.container-body > ul.nav.nav-tabs > li:nth-child(2) > a'
    EDIT_BUTTON = By.CSS_SELECTOR, '.container-body > div > table > tbody > tr:last-child > td.list-buttons-column > a'
    DELETE_BUTTON = By.CSS_SELECTOR, '.container-body table tr:last-child > td.list-buttons-column > form > button'

    DATA_USER_SELECT = By.CSS_SELECTOR, '#s2id_user .select2-chosen'
    DATA_USER_INPUT = By.ID, 's2id_autogen1_search'
    DATA_VOUCHER_SELECT = By.CSS_SELECTOR, '#s2id_voucher .select2-chosen'
    DATA_VOUCHER_INPUT = By.ID, 's2id_autogen2_search'

    ALERT = By.CSS_SELECTOR, '.container-body .alert'
    PAGE = By.CSS_SELECTOR, 'body > div.container.flex-column > div.container-body > ul.pagination > li:nth-last-child(3) > a'

    SAVE_BUTTON = By.CSS_SELECTOR, 'body > div.container.flex-column > div.container-body > form > fieldset > div:nth-child(9) > div > input.btn.btn-primary'

    def open_page(self):
        self.open(self.URL)

    def go_to_edit_page(self):
        self.click(*self.EDIT_BUTTON)

    def go_to_create_page(self):
        self.click(*self.CREATE_BUTTON)

    def create_new_user_voucher(self, user_input, voucher_input):
        self.click(*self.DATA_USER_SELECT)
        self.typing(*self.DATA_USER_INPUT, user_input + Keys.ENTER)
        time.sleep(1)
        self.click(*self.DATA_VOUCHER_SELECT)
        self.typing(*self.DATA_VOUCHER_INPUT, voucher_input + Keys.ENTER)
        time.sleep(1)

    def alert(self):
        return self.find(*self.ALERT)

    def save_user_voucher(self):
        self.click(*self.SAVE_BUTTON)

    def delete_user_voucher(self):
        self.click(*self.DELETE_BUTTON)

    def get_page(self):
        return self.find(*self.PAGE)

    def go_to_last_page(self):
        self.click(*self.PAGE)