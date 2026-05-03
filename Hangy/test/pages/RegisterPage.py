import time

from selenium.webdriver import Keys

from Hangy.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class RegisterPage(BasePage):
    URL = 'http://127.0.0.1:5000/register'

    USERNAME = By.NAME, 'username'
    PASSWORD = By.NAME, 'password'
    CONFIRM_PASSWORD = By.ID, 'confirm_password'
    FIRST_NAME = By.NAME, 'first_name'
    LAST_NAME = By.NAME, 'last_name'
    EMAIL = By.NAME, 'email'
    PHONE = By.NAME, 'phone'

    LOGIN_BUTTON = (By.CLASS_NAME, 'btn-flogin')
    REGISTER_BUTTON = (By.CLASS_NAME, 'btn-register')

    def open_page(self):
        self.open(self.URL)

    def register(self, username, password, confirm_password,first_name,last_name,email,phone):
        self.typing(*self.USERNAME, username + Keys.ENTER)
        time.sleep(1)
        self.typing(*self.PASSWORD, password + Keys.ENTER)
        self.typing(*self.CONFIRM_PASSWORD, confirm_password + Keys.ENTER)
        self.typing(*self.FIRST_NAME, first_name + Keys.ENTER)
        self.typing(*self.LAST_NAME, last_name + Keys.ENTER)
        self.typing(*self.EMAIL, email + Keys.ENTER)
        self.typing(*self.PHONE, phone + Keys.ENTER)

    def go_to_login_page(self):
        self.click(*self.LOGIN_BUTTON)