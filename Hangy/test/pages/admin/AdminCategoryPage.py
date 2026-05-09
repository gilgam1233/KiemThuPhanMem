import time

from selenium.webdriver import Keys

from Hangy.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class AdminCategoryPage(BasePage):
    URL = 'http://127.0.0.1:5000/admin/category/'

    CREATE_BUTTON = By.CSS_SELECTOR, '.container-body > ul.nav.nav-tabs > li:nth-child(2) > a'
    EDIT_BUTTON = By.CSS_SELECTOR, '.container-body > div > table > tbody > tr:last-child > td.list-buttons-column > a'
    DELETE_BUTTON = By.CSS_SELECTOR, '.container-body table tr:last-child > td.list-buttons-column > form > button'

    DATA_NAME_CATEGORY = By.ID, 'name'

    ALERT = By.CSS_SELECTOR, '.container-body .alert'

    PAGE = By.CSS_SELECTOR, 'body > div.container.flex-column > div.container-body > ul.pagination > li:nth-last-child(3) > a'


    def open_page(self):
        self.open(self.URL)

    def go_to_create_page(self):
        self.click(*self.CREATE_BUTTON)

    def go_to_edit_page(self):
        self.click(*self.EDIT_BUTTON)

    def create_new_category(self, kw):
        self.typing(*self.DATA_NAME_CATEGORY, kw + Keys.ENTER)

    def edit_category(self, kw):
        self.typing(*self.DATA_NAME_CATEGORY, kw + Keys.ENTER)

    def alert(self):
        return self.find(*self.ALERT)

    def delete_category(self):
        self.click(*self.DELETE_BUTTON)

    def get_page(self):
        return self.find(*self.PAGE)

    def go_to_last_page(self):
        self.click(*self.PAGE)