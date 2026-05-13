import time

from Hangy import app
from Hangy.test.db_helper import get_order_by_id
from Hangy.test.pages.LoginPage import LoginPage
from Hangy.test.pages.OrderHistoryPage import OrderHistoryPage
from Hangy.test.test_base import driver

def login_as(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user_0', '123')

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