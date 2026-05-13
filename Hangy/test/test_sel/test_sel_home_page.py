import time
from selenium.webdriver.common.by import By

from Hangy.test.pages.HomePage import HomePage
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user_0', '123')

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