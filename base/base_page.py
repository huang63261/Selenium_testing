import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as WD
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from util.log_utils import LogUtils

logger = LogUtils().get_log()

class BasePage(object):
    def __init__(self, driver, timeout=30) -> None:
        self.byDic = {
            'id': By.ID,
            'name': By.NAME,
            'class name': By.CLASS_NAME,
            'xpath': By.XPATH,
            'link_text': By.LINK_TEXT,
            'css': By.CSS_SELECTOR
        }
        self.base_url = "https://harvey_huang-survey2.rd1.nueip.site"
        self.time = str(time.time())
        self.driver = driver
        self.out_time = timeout

    # 抓取目前URL
    def get_current_url(self):
        return self.driver.current_url

    # 透過id, name, css, class, xpath....，查找元素
    def find_element(self, by, locator):
        try:
            logger.info("Locate by: " + by + ", locator: " + locator)
            element = WD(self.driver, self.out_time).until(lambda x: x.find_element(self.byDic.get(by), locator))
        except TimeoutException:
            logger.error("Please confirm the way of locating element.")
        else:
            return element

    # 透過id, name, css, class, xpath....，查找元素
    def find_elements(self, by, locator):
        try:
            logger.info("Locate by: " + by + ", locator: " + locator)
            element = WD(self.driver, self.out_time).until(lambda x: x.find_elements(self.byDic.get(by), locator))
        except TimeoutException:
            logger.error("Please confirm the way of locating element.")
        else:
            return element

    # 取得Selecet物件
    def get_select(self, by, locator):
        element = self.find_element(by, locator)
        return Select(element)

    # 獲取元素文本/屬性信息
    def get_text(self, by, locator):
        element = self.find_element(by, locator)
        if (element):
            text = element.text
            logger.info("Getting element text succeeded!")
            return text
        else:
            return False

    # 打開網頁
    def open_url(self, url=''):
        logger.info("Open url: " + url)
        self.driver.get(self.base_url + url)

    # 清空元素並傳值
    def send_keys(self, by, locator, keys=''):
        # 輸入操作
        logger.info("Input: " + keys)
        element = self.find_element(by, locator)
        self.sleep(0.5)
        element.clear()
        element.send_keys(keys)

    # 點擊元素
    def click(self, by, locator):
        # 點擊操作
        logger.info("Click Button: " + locator)
        self.find_element(by, locator).click()

    # 選取 Bootstrap Date Picker
    def select_date_picker(self, by, locator, date):
        element = self.find_element(by, locator)
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.click()
        action.key_down(Keys.CONTROL)
        action.send_keys('a')
        action.key_up(Keys.CONTROL)
        action.send_keys(Keys.BACK_SPACE)
        action.send_keys(date)
        action.perform()

    # 強行等待
    @staticmethod
    def sleep(num=0):
        # 強制等待
        logger.info("Process waits for " + str(num) + " seconds")
        time.sleep(num)

    # 紀錄LOG INFO
    def log_info(self, message):
        logger.info(message)

    # 紀錄LOG ERROR
    def log_error(self, message):
        logger.error(message)

    # 取得時間
    def get_time(self):
        return self.time

    # 結束 Web Driver
    def quit_browser(self):
        self.driver.quit()