import time
import uuid

from Hangy import app
from Hangy.test.db_helper import get_user_by_email, get_user_by_username, delete_user_by_email, delete_user_by_username
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.admin.AdminUserPage import AdminUserPage

from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('admin', '123')
    time.sleep(1)

def test_admin_user_create_new_user_success(driver):
    admin = AdminUserPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()
    time.sleep(1)

    random_suffix = str(uuid.uuid4())[:6]
    username = f"test_{random_suffix}"
    email = f"test{random_suffix}@gmail.com"

    admin.create_new_user(
        username,
        '123',
        email
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_username(username)
        if user: delete_user_by_username(username)

    alert = admin.alert().text
    assert 'success' in alert

def test_admin_user_create_new_user_failed_username_exists(driver):
    admin = AdminUserPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    username = 'admin'
    email = f"test{random_suffix}@gmail.com"

    admin.create_new_user(
        username,
        '123',
        email
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_email(email)
        if user: delete_user_by_email(email)

    assert 'new' in driver.current_url

def test_admin_user_create_new_user_failed_email_exists(driver):
    admin = AdminUserPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    username = f"test_{random_suffix}"
    email = 'admin@hangy.vn'

    admin.create_new_user(
        username,
        '123',
        email
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_username(username)
        if user: delete_user_by_username(username)

    assert 'new' in driver.current_url

def test_admin_user_edit_username_success(driver):
    admin = AdminUserPage(driver)
    login_as(driver)

    random_suffix = str(uuid.uuid4())[:6]
    username = f"test_{random_suffix}"
    email = f"test_{random_suffix}@gmail.com"

    admin.open_page()
    admin.go_to_create_page()
    admin.create_new_user(
        username,
        '123',
        email
    )
    time.sleep(1)
    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    admin.go_to_edit_page()
    admin.edit_user_username('test')
    time.sleep(1)

    with app.app_context():
        user = get_user_by_username('test')
        if user: delete_user_by_username('test')

    alert = admin.alert().text
    assert 'success' in alert

def test_admin_user_edit_username_failed_username_exist(driver):
    admin = AdminUserPage(driver)
    login_as(driver)

    random_suffix = str(uuid.uuid4())[:6]
    username = f"test_{random_suffix}"
    email = f"test_{random_suffix}@gmail.com"

    admin.open_page()
    admin.go_to_create_page()
    admin.create_new_user(
        username,
        '123',
        email
    )
    time.sleep(1)
    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    admin.go_to_edit_page()
    admin.edit_user_username('admin')
    time.sleep(1)

    with app.app_context():
        user = get_user_by_username(username)
        if user: delete_user_by_username(username)

    assert 'edit' in driver.current_url

def test_admin_user_delete_user_success(driver):
    admin = AdminUserPage(driver)
    login_as(driver)

    random_suffix = str(uuid.uuid4())[:6]
    username = f"test_{random_suffix}"
    email = f"test_{random_suffix}@gmail.com"

    admin.open_page()
    admin.go_to_create_page()
    admin.create_new_user(
        username,
        '123',
        email
    )
    time.sleep(2)

    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    time.sleep(1)
    admin.delete_user()
    time.sleep(1)
    driver.switch_to.alert.accept()
    time.sleep(2)

    with app.app_context():
        user = get_user_by_username(username)
        if user: delete_user_by_username(username)

    alert = admin.alert().text
    assert 'success' in alert

def test_admin_user_delete_user_failed(driver):
    admin = AdminUserPage(driver)
    login_as(driver)

    random_suffix = str(uuid.uuid4())[:6]
    username = f"test_{random_suffix}"
    email = f"test_{random_suffix}@gmail.com"

    admin.open_page()
    admin.delete_user()
    time.sleep(1)
    driver.switch_to.alert.accept()
    time.sleep(2)

    with app.app_context():
        user = get_user_by_username(username)
        if user: delete_user_by_username(username)

    alert = admin.alert().text
    assert 'thất bại' in alert