import time
import uuid

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from Hangy import app
from Hangy.test.db_helper import get_user_by_email, get_user_by_username, get_voucher_by_id, get_order_by_id, delete_user_by_email, delete_user_by_username
from Hangy.test.pages.CartPage import CartPage
from Hangy.test.pages.HomePage import HomePage
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.OrderHistoryPage import OrderHistoryPage
from Hangy.test.pages.RegisterPage import RegisterPage
from Hangy.test.test_base import driver, test_app

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


#==========================================#
# LOGIN PAGE                               #
#==========================================#

def test_login_success(driver):
    login_as(driver)

    time.sleep(1)

    hello = driver.find_element(By.CLASS_NAME, 'hello')

    assert hello.is_displayed()

def test_login_failed_with_wrong_credentials(driver):
    login = LoginPage(driver)

    login.open_page()
    login.login('ogir', '123')

    time.sleep(1)

    error = driver.find_element(By.CLASS_NAME, 'swal2-error')

    assert error.is_displayed()

def test_login_failed_with_empty_fields(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('', '123')

    time.sleep(1)

    assert "login" in driver.current_url

def test_login_go_to_register_page(driver):
    login = LoginPage(driver)
    login.open_page()

    login.go_to_register_page()

    url = driver.current_url

    assert "register" in url


#==========================================#
# REGISTER PAGE                            #
#==========================================#
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
        'Vy',
        'Tran',
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
        'Vy',
        'Tran',
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
        'Vy',
        'Tran',
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
        'Vy',
        'Tran',
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
        'Vy',
        'Tran',
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
        'Vy',
        'Tran',
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
        'Vy',
        'Tran',
        unique_email,
        'abc'
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_username(unique_username)
        assert user is None
        if user: delete_user_by_username(unique_username)

    assert "register" in driver.current_url

def test_register_failed_over_maxlength(driver):
    register = RegisterPage(driver)
    register.open_page()

    random_suffix = str(uuid.uuid4())[:6]
    unique_username = f"test_{random_suffix}"
    unique_email = f"test{random_suffix}@gmail.com"
    random_suffix_long = str(uuid.uuid4())[:60]

    register.register(
        random_suffix_long,
        '1',
        '1',
        'Vy',
        'Tran',
        unique_email,
        '0123456789'
    )
    time.sleep(2)

    with app.app_context():
        user = get_user_by_email(unique_email)
        assert user is None
        if user: delete_user_by_email(unique_email)

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
        'Tran',
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

#==========================================#
# HOMEPAGE                                 #
#==========================================#

def test_homepage_search_success(driver):
    home = HomePage(driver)

    kw='thìa gỗ'
    home.open_page()
    home.search(kw)

    time.sleep(1)

    results = driver.find_elements(By.CSS_SELECTOR, '.product')

    for r in results:
        # Lấy text của sản phẩm và chuyển hết thành chữ thường
        product_text = r.text.lower()
        kw_lower = kw.lower()

        # Kiểm tra và in ra thông báo lỗi chi tiết nếu sai
        assert kw_lower in product_text

def test_homepage_search_failed(driver):
    home = HomePage(driver)

    kw='aaa'
    home.open_page()
    home.search(kw)

    time.sleep(1)

    results = driver.find_elements(By.CSS_SELECTOR, '.product')

    assert len(results) == 0

def test_homepage_go_to_next_page(driver):
    home = HomePage(driver)

    home.open_page()
    driver.execute_script('window.scrollTo(0, 2000)')
    time.sleep(1)
    home.go_to_next_page()
    time.sleep(1)
    current_url = driver.current_url
    assert "2" in current_url

def test_homepage_data_products(driver):
    home = HomePage(driver)
    home.open_page()

    products = driver.find_elements(By.CSS_SELECTOR, '.product')

    for prod in products:
        img = prod.find_element(By.CSS_SELECTOR, '.product .img')
        assert img.get_attribute('src') != ""

        name = prod.find_element(By.CSS_SELECTOR, '.product .info h6')
        assert name.text != ""

        price = prod.find_element(By.CSS_SELECTOR, '.product .info p')
        assert price.text != ""

def test_homepage_add_to_cart_without_login(driver):
    home = HomePage(driver)

    home.open_page()
    home.add_to_cart()

    current_url = driver.current_url
    assert "login" in current_url

#==========================================#
# CART PAGE                                #
#==========================================#
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
    alert = cart.get_alert_empty_cart().text
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

    alert = cart.get_alert_empty_cart().text
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

    alert = cart.get_alert_empty_cart().text
    assert "Không có sản phẩm" in alert

def test_cart_total_amount_update(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_products_to_cart()
    time.sleep(1)

    cart.open_page()
    old_total_amount = cart.get_total_amount().text

    quantity = 2
    cart.update_quantity(quantity)
    new_total_amount = cart.get_total_amount().text

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
        db_vouchers = get_voucher_by_id(2)

    assert set(ui_vouchers) == set(db_vouchers)

def test_cart_select_voucher_update_final_amount(driver):
    home = HomePage(driver)
    cart = CartPage(driver)

    login_as(driver)
    time.sleep(1)

    home.add_to_cart()
    time.sleep(1)

    cart.open_page()
    old_final_amount = cart.get_final_amount().text

    vouchers = Select(cart.get_voucher_select())
    vouchers.select_by_index(1)
    time.sleep(1)

    discount = cart.get_voucher_discount().text
    assert discount != 0

    new_final_amount = cart.get_final_amount().text
    assert new_final_amount < old_final_amount

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
    alert = cart.get_alert_empty_cart().text
    assert 'Không có sản phẩm' in alert

#==========================================#
# ORDER HISTORY PAGE                       #
#==========================================#
def test_order_history(driver):
    login_as(driver)
    time.sleep(1)

    order_history = OrderHistoryPage(driver)
    order_history.open_page()

    with app.app_context():
        db_orders = get_order_by_id(2)
        print(db_orders)
    tmp_orders = order_history.get_order_history()
    orders = [t.text for t in tmp_orders]
    print(orders)

    # set: so sánh không quan tâm đến thứ tự sắp xếp
    assert set(db_orders) == set(orders)
