from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ChromeDriver:
    def __init__(self, headless=False):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        if headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

class FirefoxDriver:
    def __init__(self, headless=False):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--start-maximized")
        if headless:
            firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=firefox_options)

class DriverFactory:
    @staticmethod
    def create_driver(browser="chrome", headless=False):
        if browser.lower() == "chrome":
            return ChromeDriver(headless=headless).driver
        elif browser.lower() == "firefox":
            return FirefoxDriver(headless=headless).driver
        else:
            raise ValueError(f"Unsupported browser: {browser}")

def quit_driver(driver):
    driver.quit()