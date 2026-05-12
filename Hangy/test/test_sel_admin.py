import time
import uuid
from datetime import datetime, timedelta

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from sqlalchemy import null

from Hangy import app
from Hangy.test.db_helper import get_user_by_email, get_user_by_username, get_voucher_by_id, get_order_by_id, \
    delete_user_by_email, delete_user_by_username, get_category_by_name, delete_category_by_name, get_product_by_name, \
    delete_product_by_name, get_voucher_by_code, delete_voucher_by_code
from Hangy.test.pages.CartPage import CartPage
from Hangy.test.pages.HomePage import HomePage
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.admin.AdminCategoryPage import AdminCategoryPage
from Hangy.test.pages.admin.AdminIndexPage import AdminIndexPage
from Hangy.test.pages.admin.AdminOrderPage import AdminOrderPage
from Hangy.test.pages.admin.AdminProductPage import AdminProductPage
from Hangy.test.pages.admin.AdminUserPage import AdminUserPage
from Hangy.test.pages.admin.AdminUserVoucherPage import AdminUserVoucherPage
from Hangy.test.pages.admin.AdminVoucherPage import AdminVoucherPage

from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('admin', '123')
    time.sleep(1)

#==========================================#
# ADMIN INDEX PAGE                         #
#==========================================#
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

#==========================================#
# USER PAGE                                #
#==========================================#
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

    alert = admin.alert().text
    assert 'Fail' in alert

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

    alert = admin.alert().text
    assert 'Fail' in alert

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

    alert = admin.alert().text
    assert 'Fail' in alert

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

#==========================================#
# CATEGORY PAGE                            #
#==========================================#
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

#==========================================#
# PRODUCT PAGE                             #
#==========================================#
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
        user = get_product_by_name(name)
        if user: delete_product_by_name(name)

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
        user = get_product_by_name('test')
        if user: delete_product_by_name('test')

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

#==========================================#
# ORDER PAGE                               #
#==========================================#
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

#==========================================#
# VOUCHER PAGE                             #
#==========================================#
def test_admin_voucher_create_new_voucher_success(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'PERCENT'
    discount_value = '35'
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    alert = admin.alert().text
    assert 'success' in alert

    with app.app_context():
        voucher = get_voucher_by_code(code)
        if voucher:
            delete_voucher_by_code(code)

def test_admin_voucher_create_new_voucher_failed_missing_required_fields(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'PERCENT'
    discount_value = ''
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    assert 'new' in driver.current_url

    with app.app_context():
        voucher = get_voucher_by_code(code)
        if voucher:
            delete_voucher_by_code(code)

def test_admin_voucher_create_new_voucher_failed_end_date(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'PERCENT'
    discount_value = '30'
    enddate = (datetime.today() - timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    assert 'new' in driver.current_url

    with app.app_context():
        voucher = get_voucher_by_code(code)
        if voucher:
            delete_voucher_by_code(code)

def test_admin_voucher_create_new_voucher_failed_discount_over_fifty_percent(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'PERCENT'
    discount_value = '70'
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    alert = admin.alert().text
    assert 'Lỗi' in alert

    assert 'new' in driver.current_url

    with app.app_context():
        voucher = get_voucher_by_code(code)
        if voucher:
            delete_voucher_by_code(code)

def test_admin_voucher_create_new_voucher_failed_code_exists(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    code = 'TEST_BASE'
    discount_type = 'PERCENT'
    discount_value = '30'
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    admin.go_to_create_page()
    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    ư

    assert 'new' in driver.current_url

def test_admin_voucher_create_new_voucher_failed_discount_negative_value(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'AMOUNT'
    discount_value = '-1'
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    assert 'new' in driver.current_url

    with app.app_context():
        voucher = get_voucher_by_code(code)
        if voucher:
            delete_voucher_by_code(code)

def test_admin_voucher_edit_discount_value_success(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'PERCENT'
    discount_value = '35'
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    admin.go_to_edit_page()
    admin.edit_voucher_discount_value('50')
    time.sleep(1)

    alert = admin.alert().text
    assert 'success' in alert

    with app.app_context():
        voucher = get_voucher_by_code(code)
        if voucher:
            delete_voucher_by_code(code)

def test_admin_voucher_edit_discount_value_failed(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'PERCENT'
    discount_value = '35'
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    admin.go_to_edit_page()
    admin.edit_voucher_discount_value('51')
    time.sleep(1)

    alert = admin.alert().text
    assert 'Lỗi' in alert

    with app.app_context():
        voucher = get_voucher_by_code(code)
        if voucher:
            delete_voucher_by_code(code)

def test_admin_voucher_delete_voucher_success(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'PERCENT'
    discount_value = '35'
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    admin = AdminUserVoucherPage(driver)
    admin.open_page()
    admin.go_to_create_page()
    admin.create_new_user_voucher('2', code)
    admin.save_user_voucher()
    time.sleep(2)

    admin = AdminIndexPage(driver)
    admin.open_page()
    admin.logout()

    home = HomePage(driver)
    cart = CartPage(driver)

    login = LoginPage(driver)
    login.open_page()
    login.login('user_0', '123')
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()
    vouchers = Select(cart.get_voucher_select())
    last_index = len(vouchers.options) - 1
    vouchers.select_by_index(last_index)
    time.sleep(1)
    cart.pay()
    time.sleep(1)

    home.logout()

    admin = AdminOrderPage(driver)
    login_as(driver)
    admin.open_page()
    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    admin.go_to_edit_page()
    time.sleep(2)
    admin.edit_status_order('CONFIRMED')
    admin.save_order()
    time.sleep(1)

    admin = AdminVoucherPage(driver)

    admin.open_page()
    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    time.sleep(1)
    admin.delete_voucher()
    driver.switch_to.alert.accept()
    time.sleep(1)

    alert = admin.alert().text
    assert 'success' in alert

def test_admin_voucher_delete_voucher_failed_using_voucher(driver):
    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    admin.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'PERCENT'
    discount_value = '35'
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    admin = AdminUserVoucherPage(driver)
    admin.open_page()
    admin.go_to_create_page()
    admin.create_new_user_voucher('2',code)
    admin.save_user_voucher()
    time.sleep(2)

    admin = AdminIndexPage(driver)
    admin.open_page()
    admin.logout()

    home = HomePage(driver)
    cart = CartPage(driver)

    login = LoginPage(driver)
    login.open_page()
    login.login('user_0', '123')
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()
    vouchers = Select(cart.get_voucher_select())
    last_index = len(vouchers.options) - 1
    vouchers.select_by_index(last_index)
    time.sleep(1)
    cart.pay()
    time.sleep(1)

    home.logout()

    admin = AdminVoucherPage(driver)
    login_as(driver)

    admin.open_page()
    page = admin.get_page()
    if page:
        admin.go_to_last_page()
    time.sleep(1)
    admin.delete_voucher()
    driver.switch_to.alert.accept()
    time.sleep(1)

    alert = admin.alert().text
    assert 'thất bại' in alert
