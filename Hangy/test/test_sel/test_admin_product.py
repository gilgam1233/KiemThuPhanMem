import time
import uuid
from Hangy import app
from Hangy.test.db_helper import get_product_by_name, delete_product_by_name
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.admin.AdminProductPage import AdminProductPage

from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('admin', '123')
    time.sleep(1)

def test_admin_product_create_new_product_success(driver):
    admin = AdminProductPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    name = f"test_{random_suffix}"
    price = '70000'

    admin.create_new_product(
        name,
        price
    )
    time.sleep(2)

    with app.app_context():
        prod = get_product_by_name(name)
        if prod: delete_product_by_name(name)

    alert = admin.alert().text
    assert 'success' in alert

def test_admin_product_edit_name_success(driver):
    admin = AdminProductPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    name = f"test_{random_suffix}"
    price = '70000'

    admin.create_new_product(
        name, price
    )
    time.sleep(2)
    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    admin.go_to_edit_page()
    time.sleep(1)
    admin.edit_name_product('test')
    time.sleep(1)

    with app.app_context():
        prod = get_product_by_name('test')
        if prod: delete_product_by_name('test')

    alert = admin.alert().text
    assert 'success' in alert

def test_admin_product_delete_product_success(driver):
    admin = AdminProductPage(driver)
    login_as(driver)

    random_suffix = str(uuid.uuid4())[:6]
    name = f"test_{random_suffix}"
    price = '70000'

    admin.open_page()
    admin.go_to_create_page()
    admin.create_new_product(
        name,price
    )
    time.sleep(2)

    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    admin.delete_product()
    time.sleep(1)
    driver.switch_to.alert.accept()
    time.sleep(2)

    alert = admin.alert().text
    assert 'success' in alert

def test_admin_product_delete_product_failed(driver):
    admin = AdminProductPage(driver)
    login_as(driver)

    admin.open_page()

    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    admin.delete_product()
    time.sleep(1)
    driver.switch_to.alert.accept()
    time.sleep(2)

    alert = admin.alert().text
    assert 'thất bại' in alert