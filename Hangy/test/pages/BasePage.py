class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return self.driver.find_element(by, value)

    def finds(self, by, value):
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        self.find(by, value).click()

    def typing(self, by, value, text):
        e = self.find(by, value)
        e.clear()
        e.send_keys(text)

    def accept_browser_alert(self):
        self.driver.switch_to.alert.accept()

    def dismiss_browser_alert(self):
        self.driver.switch_to.alert.dismiss()
