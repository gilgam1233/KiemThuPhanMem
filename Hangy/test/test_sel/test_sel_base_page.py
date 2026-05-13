import time
from Hangy.test.pages.HomePage import HomePage
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user_0', '123')

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

def test_click_cart_without_login(driver):
    home = HomePage(driver)

    home.open_page()
    home.go_to_cart()

    current_url = driver.current_url
    assert "login" in current_url

def test_click_cart_with_login(driver):
    home = HomePage(driver)

    login_as(driver)

    time.sleep(1)

    home.go_to_cart()

    current_url = driver.current_url
    assert "cart" in current_url