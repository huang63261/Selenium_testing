from base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class LoginPage(BasePage):
    """存取控件 & 元素操作"""
    comp_input = (By.ID, "dept_input")
    username_input = (By.ID, "username_input")
    password_input = (By.ID, "password-input")
    login_button = (By.ID, "login-button")
    error_msg = (By.CLASS_NAME, "ctrl-error-msg")

    def __init__(self, driver, timeout=3) -> None:
        super().__init__(driver, timeout)

    """登入流程"""
    def login(self,company, username, password):
        self.open_url()
        self.send_company(company)
        self.send_username(username)
        self.send_password(password)
        self.click_login_btn()
        msg = self.get_login_status()

        return msg

    def quit(self):
        self.quit_browser()

    def send_company(self, company):
        self.send_keys(*LoginPage.comp_input, company)

    def send_username(self, username):
        self.send_keys(*LoginPage.username_input, username)

    def send_password(self, password):
        self.send_keys(*LoginPage.password_input, password)

    def click_login_btn(self):
        self.click(*LoginPage.login_button)

    def get_login_status(self):
        try:
            error_msg = self.driver.find_element(*LoginPage.error_msg).text
            if error_msg:
                self.log_error(error_msg)
                return False
        except NoSuchElementException:
            self.log_info("成功登入")
            return True

if __name__ == "__main__":
    pass