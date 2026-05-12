import time
import uuid
from selenium.webdriver.common.by import By

from Hangy import app
from Hangy.test.db_helper import get_user_by_email, get_user_by_username, delete_user_by_email, delete_user_by_username
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.RegisterPage import RegisterPage
from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user_0', '123')

def test_register_success(driver):
    register = RegisterPage(driver)
    register.open_page()

    random_suffix = str(uuid.uuid4())[:6]
    unique_username = f"test_{random_suffix}"
    unique_email = f"test{random_suffix}@gmail.com"

    register.register(
        unique_username,
        '1',
        '1',
        'Ten',
        'Ho',
        unique_email,
        '0123456789'
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_username(unique_username)
        assert user is not None
        if user: delete_user_by_username(unique_username)

    assert "login" in driver.current_url

def test_register_failed_missing_required_fields(driver):
    register = RegisterPage(driver)
    register.open_page()

    random_suffix = str(uuid.uuid4())[:6]
    unique_email = f"test{random_suffix}@gmail.com"

    register.register(
        '',
        '1',
        '1',
        'Ten',
        'Ho',
        unique_email,
        '0123456789'
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_email(unique_email)
        assert user is None
        if user: delete_user_by_email(unique_email)

    assert "register" in driver.current_url

def test_register_failed_username_exists(driver):
    register = RegisterPage(driver)
    register.open_page()

    random_suffix = str(uuid.uuid4())[:6]
    unique_email = f"test{random_suffix}@gmail.com"

    register.register(
        'admin',
        '1',
        '1',
        'Ten',
        'Ho',
        unique_email,
        '0123456789'
    )
    time.sleep(2)

    err = driver.find_element(By.ID, 'swal2-html-container')
    assert "Username" in err.text

    with app.app_context():
        user = get_user_by_email(unique_email)
        assert user is None
        if user: delete_user_by_email(unique_email)

    assert "register" in driver.current_url

def test_register_failed_password_missmatch(driver):
    register = RegisterPage(driver)
    register.open_page()

    random_suffix = str(uuid.uuid4())[:6]
    unique_username = f"test_{random_suffix}"
    unique_email = f"test{random_suffix}@gmail.com"

    register.register(
        unique_username,
        '1',
        '2',
        'Ten',
        'Ho',
        unique_email,
        '0123456789'
    )
    time.sleep(2)

    err = driver.find_element(By.ID, 'swal2-html-container')
    assert "Mật khẩu" in err.text

    with app.app_context():
        user = get_user_by_email(unique_email)
        assert user is None
        if user: delete_user_by_email(unique_email)

    assert "register" in driver.current_url

def test_register_failed_email_exists(driver):
    register = RegisterPage(driver)
    register.open_page()

    random_suffix = str(uuid.uuid4())[:6]
    unique_username = f"test_{random_suffix}"

    register.register(
        unique_username,
        '1',
        '1',
        'Ten',
        'Ho',
        'admin@hangy.vn',
        '0123456789'
    )
    time.sleep(2)

    err = driver.find_element(By.ID, 'swal2-html-container')
    assert "Email" in err.text

    with app.app_context():
        user = get_user_by_username(unique_username)
        assert user is None
        if user: delete_user_by_username(unique_username)

    assert "register" in driver.current_url

def test_register_failed_invalid_email(driver):
    register = RegisterPage(driver)
    register.open_page()

    random_suffix = str(uuid.uuid4())[:6]
    unique_username = f"test_{random_suffix}"
    unique_email = f"test{random_suffix}@"

    register.register(
        unique_username,
        '1',
        '1',
        'Ten',
        'Ho',
        unique_email,
        '0123456789'
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_username(unique_username)
        assert user is None
        if user: delete_user_by_username(unique_username)

    assert "register" in driver.current_url

def test_register_failed_invalid_phone(driver):
    register = RegisterPage(driver)
    register.open_page()

    random_suffix = str(uuid.uuid4())[:6]
    unique_username = f"test_{random_suffix}"
    unique_email = f"test{random_suffix}@gmail.com"

    register.register(
        unique_username,
        '1',
        '1',
        'Ten',
        'Ho',
        unique_email,
        'abc'
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_username(unique_username)
        assert user is None
        if user: delete_user_by_username(unique_username)

    assert "register" in driver.current_url

def test_register_failed_whitespaces_fields(driver):
    register = RegisterPage(driver)
    register.open_page()

    random_suffix = str(uuid.uuid4())[:6]
    unique_username = f"test_{random_suffix}"
    unique_email = f"test{random_suffix}@gmail.com"

    register.register(
        unique_username,
        '1',
        '1',
        '   ',
        'Ho',
        unique_email,
        '0123456789'
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_email(unique_email)
        assert user is None
        if user: delete_user_by_email(unique_email)

    assert "register" in driver.current_url

def test_register_go_to_login_page(driver):
    register = RegisterPage(driver)
    register.open_page()

    driver.execute_script('window.scrollTo(0, 2000)')
    time.sleep(1)

    register.go_to_login_page()

    assert "login" in driver.current_url