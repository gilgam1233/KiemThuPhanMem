import time
import uuid
from datetime import datetime, timedelta
from selenium.webdriver.support.select import Select

from Hangy import app
from Hangy.test.db_helper import get_voucher_by_code, delete_voucher_by_code
from Hangy.test.pages.CartPage import CartPage
from Hangy.test.pages.HomePage import HomePage
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.admin.AdminIndexPage import AdminIndexPage
from Hangy.test.pages.admin.AdminOrderPage import AdminOrderPage
from Hangy.test.pages.admin.AdminUserVoucherPage import AdminUserVoucherPage
from Hangy.test.pages.admin.AdminVoucherPage import AdminVoucherPage

from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('admin', '123')
    time.sleep(1)

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
    admin_v = AdminVoucherPage(driver)
    login_as(driver)

    admin_v.open_page()
    admin_v.go_to_create_page()

    random_suffix = str(uuid.uuid4())[:6]
    code = f"TEST_VOUCHER_{random_suffix}"
    discount_type = 'PERCENT'
    discount_value = '35'
    enddate = (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p')

    admin_v.create_new_voucher(
        code, discount_type, discount_value, enddate
    )
    time.sleep(2)

    admin_uv = AdminUserVoucherPage(driver)
    admin_uv.open_page()
    admin_uv.go_to_create_page()
    admin_uv.create_new_user_voucher('2', code)
    admin_uv.save_user_voucher()
    time.sleep(2)

    admin_i = AdminIndexPage(driver)
    admin_i.open_page()
    admin_i.logout()

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

    admin_o = AdminOrderPage(driver)
    login_as(driver)
    admin_o.open_page()
    page = admin_o.get_page()
    if page:
        admin_o.go_to_last_page()
    admin_o.go_to_edit_page()
    time.sleep(2)
    admin_o.edit_status_order('CONFIRMED')
    admin_o.save_order()
    time.sleep(1)

    admin_v.open_page()
    page = admin_v.get_page()
    if page:
        admin_v.go_to_last_page()
    time.sleep(1)
    admin_v.delete_voucher()
    driver.switch_to.alert.accept()
    time.sleep(1)

    admin_uv.open_page()
    admin_uv.go_to_last_page()
    admin_uv.delete_user_voucher()
    driver.switch_to.alert.accept()
    time.sleep(1)

    admin_v.open_page()
    admin_v.go_to_last_page()
    admin_v.delete_voucher()
    driver.switch_to.alert.accept()
    time.sleep(1)

    alert = admin_v.alert().text


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