import time
from selenium.webdriver.common.by import By

from Hangy.test.pages.HomePage import HomePage
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user_0', '123')
    time.sleep(1)

def test_click_login_button(driver):
    home = HomePage(driver)

    home.open_page()
    home.go_to_login()

    current_url = driver.current_url
    assert "login" in current_url

def test_click_logout_button(driver):
    home = HomePage(driver)

    login_as(driver)

    time.sleep(1)

    home.logout()

    assert "login" in driver.current_url

def test_login_success(driver):
    login_as(driver)

    hello = driver.find_element(By.CLASS_NAME, 'hello')

    assert hello.is_displayed()

def test_login_failed_with_wrong_credentials(driver):
    login = LoginPage(driver)

    login.open_page()
    login.login('aaa', '123')

    time.sleep(1)

    error = driver.find_element(By.CLASS_NAME, 'swal2-error')

    assert error.is_displayed()

def test_login_failed_with_empty_fields(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('', '123')

    time.sleep(1)

    assert "login" in driver.current_url

def test_login_go_to_register_page(driver):
    login = LoginPage(driver)
    login.open_page()

    login.go_to_register_page()

    assert "register" in driver.current_url