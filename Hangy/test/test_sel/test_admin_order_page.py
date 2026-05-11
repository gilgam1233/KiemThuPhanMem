import time
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.admin.AdminOrderPage import AdminOrderPage

from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('admin', '123')
    time.sleep(1)

def test_admin_order_create_and_delete_new_order_(driver):
    admin = AdminOrderPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    total = '100000'
    final = '70000'
    user = '2'

    admin.create_new_order(
        total,final,user
    )
    time.sleep(2)

    alert = admin.alert().text
    assert 'success' in alert

    admin.open_page()
    admin.delete_order()
    driver.switch_to.alert.accept()