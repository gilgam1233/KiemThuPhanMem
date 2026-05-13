import time

from selenium.webdriver import Keys

from Hangy.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class AdminVoucherPage(BasePage):
    URL = 'http://127.0.0.1:5000/admin/voucher'

    CREATE_BUTTON = By.CSS_SELECTOR, '.container-body > ul.nav.nav-tabs > li:nth-child(2) > a'
    EDIT_BUTTON = By.CSS_SELECTOR, '.container-body > div > table > tbody > tr:last-child > td.list-buttons-column > a'
    DELETE_BUTTON = By.CSS_SELECTOR, '.container-body table tr:last-child > td.list-buttons-column > form > button'

    DATA_CODE = By.ID, 'code'
    DATA_DISCOUNT_TYPE_SELECT = By.CSS_SELECTOR, '#s2id_discount_type .select2-chosen'
    DATA_DISCOUNT_TYPE_INPUT = By.CSS_SELECTOR, '.select2-search .select2-input'
    DATA_DISCOUNT_VALUE = By.ID, 'discount_value'
    DATA_END_DATE = By.ID, 'end_date'

    ALERT = By.CSS_SELECTOR, '.container-body .alert'
    PAGE = By.CSS_SELECTOR, 'body > div.container.flex-column > div.container-body > ul.pagination > li:nth-last-child(3) > a'


    def open_page(self):
        self.open(self.URL)

    def go_to_create_page(self):
        self.click(*self.CREATE_BUTTON)

    def go_to_edit_page(self):
        self.click(*self.EDIT_BUTTON)

    def typing_end_date(self, end_date):
        e= self.find(*self.DATA_END_DATE)
        e.click()
        # Cắt chuỗi ra làm 3 phần
        date_part = end_date[:8]  # Lấy mm-dd-YYYY
        time_part = end_date[8:12]  # Lấy HH:MM
        ampm_part = end_date[12:]  # Lấy PM/AM

        # Thực hiện gõ từng phần một
        e.send_keys(date_part)
        e.send_keys(Keys.TAB)  # ÉP trình duyệt nhảy sang ô Giờ/Phút
        e.send_keys(time_part)
        e.send_keys(ampm_part)
        e.send_keys(Keys.ENTER)

    def create_new_voucher(self, code,discount_type,discount_value,end_date):
        self.typing(*self.DATA_CODE, code + Keys.ENTER)
        self.click(*self.DATA_DISCOUNT_TYPE_SELECT)
        self.typing(*self.DATA_DISCOUNT_TYPE_INPUT, discount_type + Keys.ENTER)
        time.sleep(1)
        self.typing(*self.DATA_DISCOUNT_VALUE, discount_value + Keys.ENTER)
        self.typing_end_date(end_date)
        time.sleep(1)

    def edit_voucher_discount_value(self, kw):
        self.typing(*self.DATA_DISCOUNT_VALUE, kw + Keys.ENTER)

    def alert(self):
        return self.find(*self.ALERT)

    def delete_voucher(self):
        self.click(*self.DELETE_BUTTON)

    def get_page(self):
        return self.find(*self.PAGE)

    def go_to_last_page(self):
        self.click(*self.PAGE)