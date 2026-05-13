import time
import uuid

from Hangy import app
from Hangy.test.db_helper import get_category_by_name, delete_category_by_name
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.admin.AdminCategoryPage import AdminCategoryPage

from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('admin', '123')
    time.sleep(1)

def test_admin_category_create_new_category_success(driver):
    admin = AdminCategoryPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    name = f"test_{random_suffix}"

    admin.create_new_category(
        name
    )
    time.sleep(2)

    with app.app_context():
        user = get_category_by_name(name)
        if user: delete_category_by_name(name)

    alert = admin.alert().text
    assert 'success' in alert

def test_admin_category_create_new_category_failed_name_exists(driver):
    admin = AdminCategoryPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    name = 'Inox'

    admin.create_new_category(
        name
    )
    time.sleep(2)

    alert = admin.alert().text
    assert 'Fail' in alert

def test_admin_category_edit_name_success(driver):
    admin = AdminCategoryPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    name = f"test_{random_suffix}"

    admin.create_new_category(
        name
    )
    time.sleep(2)

    admin.go_to_edit_page()
    admin.edit_category('test')
    time.sleep(1)

    with app.app_context():
        user = get_category_by_name('test')
        if user: delete_category_by_name('test')

    alert = admin.alert().text
    assert 'success' in alert

def test_admin_category_edit_name_failed_name_exist(driver):
    admin = AdminCategoryPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    name = f"test_{random_suffix}"

    admin.create_new_category(
        name
    )
    time.sleep(2)

    admin.go_to_edit_page()
    admin.edit_category('Inox')
    time.sleep(1)

    with app.app_context():
        user = get_category_by_name(name)
        if user: delete_category_by_name(name)

    alert = admin.alert().text
    assert 'Fail' in alert

def test_admin_category_delete_category(driver):
    admin = AdminCategoryPage(driver)
    login_as(driver)

    random_suffix = str(uuid.uuid4())[:6]
    name = f"test_{random_suffix}"

    admin.open_page()
    admin.go_to_create_page()
    admin.create_new_category(
        name
    )
    time.sleep(2)

    admin.delete_category()
    time.sleep(1)
    driver.switch_to.alert.accept()
    time.sleep(2)

    alert = admin.alert().text
    assert 'success' in alert