import time

from selenium.webdriver import Keys

from Hangy.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class AdminIndexPage(BasePage):
    URL = 'http://127.0.0.1:5000/admin/'

    USER_PAGE = By.CSS_SELECTOR, '#admin-navbar-collapse li:nth-child(2) > a'
    LOGOUT_BUTTON = By.CSS_SELECTOR, '#admin-navbar-collapse > ul.nav.navbar-nav.navbar-right > li:nth-child(2) > a'

    USER_INFO = By.CSS_SELECTOR, '.container-body > div:nth-child(1) table > tbody > tr > td'

    CREATE_USER = By.CSS_SELECTOR, '.container-body > div:nth-child(2) > div > div > div:nth-child(1) > a'


    def open_page(self):
        self.open(self.URL)

    def go_to_user_page(self):
        self.click(*self.USER_PAGE)

    def get_user_info(self):
        return self.finds(*self.USER_INFO)

    def logout(self):
        self.click(*self.LOGOUT_BUTTON)

    def click_create_user(self):
        self.click(*self.CREATE_USER)