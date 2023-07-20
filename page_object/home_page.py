from base.base_page import BasePage
## BY: 也就是依照條件尋找元素中XPATH、CLASS NAME、ID、CSS選擇器等都會用到的Library
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class HomePage(BasePage):
    url = "/home"
    """存取控件 & 元素操作"""
    username = (By.CSS_SELECTOR, ".profiles_block--name")

    def go_home(self):
        self.open_url(url=self.url)