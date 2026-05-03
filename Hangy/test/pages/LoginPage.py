from selenium.webdriver import Keys

from Hangy.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    URL = 'http://127.0.0.1:5000/login'

    USERNAME = By.NAME, 'username'
    PASSWORD = By.NAME, 'password'

    LOGIN_BUTTON = (By.CLASS_NAME, 'btn-login')
    REGISTER_BUTTON = (By.CLASS_NAME, 'btn-register')

    def open_page(self):
        self.open(self.URL)

    def login(self, username, password):
        self.typing(*self.USERNAME, username + Keys.ENTER)
        self.typing(*self.PASSWORD, password + Keys.ENTER)

    def go_to_register_page(self):
        self.click(*self.REGISTER_BUTTON)