import time
import uuid
from datetime import datetime, timedelta
from Hangy.routes.main import voucher_services

from selenium.common import NoSuchElementException
from selenium.webdriver.support.select import Select

from Hangy import app
from Hangy.test.db_helper import get_voucher_by_id
from Hangy.test.pages.CartPage import CartPage
from Hangy.test.pages.HomePage import HomePage
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.admin.AdminIndexPage import AdminIndexPage
from Hangy.test.pages.admin.AdminUserVoucherPage import AdminUserVoucherPage
from Hangy.test.pages.admin.AdminVoucherPage import AdminVoucherPage
from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user_0', '123')

def test_cart_add_to_cart_with_login(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)

    time.sleep(1)

    old_quantity = home.get_cart_number()
    home.add_to_cart()
    home_product = home.get_name_product().text
    time.sleep(1)
    new_quantity = home.get_cart_number()
    assert new_quantity == old_quantity + 1

    cart.open_page()
    time.sleep(1)
    cart_product = cart.get_name_product().text
    assert home_product == cart_product

def test_cart_empty_cart(driver):
    cart = CartPage(driver)
    home = HomePage(driver)

    login_as(driver)
    time.sleep(1)

    home.go_to_cart()
    alert = cart.get_alert().text
    assert "Không có sản phẩm" in alert

def test_cart_update_quantity(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)
    old_quantity = home.get_cart_number()

    cart.open_page()
    old_amount = cart.get_amount_product().text

    quantity = 3
    cart.update_quantity(quantity)
    new_quantity = cart.get_cart_number()
    new_amount = cart.get_amount_product().text
    time.sleep(1)

    assert new_quantity != old_quantity
    assert old_amount != new_amount

def test_cart_delete_product_confirm(driver):
    home = HomePage(driver)
    login_as(driver)
    time.sleep(1)

    home.add_products_to_cart()
    time.sleep(1)

    cart = CartPage(driver)
    cart.open_page()

    cart.delete_product()
    cart.confirm_delete_cart()
    time.sleep(1)

    try:
        cart.get_first_cart_item() #Tim cart1 nhung da xoa nen catch except
        print("Xoá sản phẩm thất bại")
        assert False
    except NoSuchElementException:
        assert True

def test_cart_delete_product_to_empty_cart(driver):
    home = HomePage(driver)
    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart = CartPage(driver)
    cart.open_page()

    cart.delete_product()
    cart.confirm_delete_cart()
    time.sleep(1)

    alert = cart.get_alert().text
    assert 'Không có sản phẩm' in alert

def test_cart_delete_product_cancel(driver):
    home = HomePage(driver)
    login_as(driver)
    time.sleep(1)

    home.add_products_to_cart()
    time.sleep(1)

    cart = CartPage(driver)
    cart.open_page()

    cart.delete_product()
    cart.cancel_delete_cart()
    time.sleep(3)

    try:
        cart.get_first_cart_item()  # Tim cart1 nhung chua xoa nen khong catch except
        assert True
    except NoSuchElementException:
        assert False

def test_cart_update_quantity_le0_cancel_del_product(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)
    old_quantity = home.get_cart_number()

    cart.open_page()
    old_amount = cart.get_amount_product().text

    quantity = 0
    cart.update_quantity(quantity)
    cart.cancel_delete_cart()
    new_quantity = cart.get_cart_number()
    new_amount = cart.get_amount_product().text
    time.sleep(2)

    assert new_quantity == old_quantity
    assert old_amount == new_amount

def test_cart_update_quantity_le0_confirm_del_product(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()

    quantity = 0
    cart.update_quantity(quantity)
    cart.confirm_delete_cart()
    time.sleep(1)

    alert = cart.get_alert().text
    assert "Không có sản phẩm" in alert

def test_cart_total_amount_update(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_products_to_cart()
    time.sleep(1)

    cart.open_page()
    old_total_amount = cart.get_total_amount()

    quantity = 2
    cart.update_quantity(quantity)
    new_total_amount = cart.get_total_amount()

    assert new_total_amount > old_total_amount

def test_cart_load_vouchers(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()

    vouchers = Select(cart.get_voucher_select())
    ui_vouchers = [
        option.get_attribute("value")
        for option in vouchers.options
        if option.get_attribute("value") != ""
    ]

    with app.app_context():
        db_vouchers = get_voucher_by_id(user_id=2)

    assert set(ui_vouchers) == set(db_vouchers)

def test_cart_select_voucher_update_final_amount(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()
    old_final_amount = cart.get_final_amount()

    vouchers = Select(cart.get_voucher_select())
    vouchers.select_by_index(1)
    time.sleep(1)

    discount = cart.get_voucher_discount()
    assert discount != 0

    new_final_amount = cart.get_final_amount()
    assert new_final_amount < old_final_amount

def test_cart_recalculate_voucher_when_quantity_changes(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()

    vouchers = Select(cart.get_voucher_select())
    vouchers.select_by_index(1)
    time.sleep(1)

    old_discount = cart.get_voucher_discount()

    cart.update_quantity(3)
    new_discount = cart.get_voucher_discount()

    assert old_discount != new_discount

def test_cart_switch_vouchers_continuously(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()

    vouchers = Select(cart.get_voucher_select())
    vouchers.select_by_index(1)
    assert cart.get_voucher_discount() > 0

    vouchers.select_by_index(0)
    assert cart.get_voucher_discount() == 0

    vouchers.select_by_index(2)
    assert cart.get_voucher_discount() > 0

def test_cart_voucher_amount_greater_than_total(driver):
    home = HomePage(driver)
    cart = CartPage(driver)
    login = LoginPage(driver)
    admin_v = AdminVoucherPage(driver)

    login.open_page()
    login.login('admin', '123')
    time.sleep(1)
    admin_v.open_page()
    time.sleep(1)

    admin_v.go_to_create_page()
    admin_v.create_new_voucher('GIAM500K', 'AMOUNT', '500000',
                               (datetime.today() + timedelta(days=1)).strftime('%m%d%Y%I%M%p'))

    admin_uv = AdminUserVoucherPage(driver)
    admin_uv.open_page()
    admin_uv.go_to_create_page()
    admin_uv.create_new_user_voucher('2', 'GIAM500K')
    admin_uv.save_user_voucher()
    time.sleep(2)

    admin = AdminIndexPage(driver)
    admin.logout()

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()

    vouchers = Select(cart.get_voucher_select())
    vouchers.select_by_index(len(vouchers.options) - 1)
    time.sleep(1)
    final_amount = cart.get_final_amount()
    assert final_amount == 0
    home.logout()

    admin_uv.open_page()
    admin_uv.go_to_last_page()
    admin_uv.delete_user_voucher()
    driver.switch_to.alert.accept()

    admin_v.open_page()
    admin_v.go_to_last_page()
    admin_v.delete_voucher()
    driver.switch_to.alert.accept()
    time.sleep(1)

def test_cart_pay(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()
    cart.pay()
    time.sleep(1)
    assert 'order_history' in driver.current_url

    cart_number = cart.get_cart_number()
    assert cart_number == 0

    cart.open_page()
    alert = cart.get_alert().text
    assert 'Không có sản phẩm' in alert