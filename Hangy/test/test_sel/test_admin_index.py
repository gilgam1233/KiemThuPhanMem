import time
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.admin.AdminIndexPage import AdminIndexPage

from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('admin', '123')
    time.sleep(1)

def test_admin_index_logout(driver):
    admin = AdminIndexPage(driver)

    login_as(driver)

    admin.logout()

    assert 'login' in driver.current_url

def test_admin_index_side_navbar(driver):
    login_as(driver)
    admin = AdminIndexPage(driver)

    admin.go_to_user_page()

    assert 'admin/user' in driver.current_url

def test_admin_index_click_create_user(driver):
    admin = AdminIndexPage(driver)
    login_as(driver)

    admin.click_create_user()

    assert 'admin/user/new' in driver.current_url

def test_admin_index_user_info(driver):
    admin = AdminIndexPage(driver)
    login_as(driver)

    info = admin.get_user_info()

    for i in info:
        assert i is not None