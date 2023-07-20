import pytest
import os
import dotenv
from driver.driver import DriverFactory, quit_driver
from page_object.login_page import LoginPage

@pytest.fixture(scope='session')
def driver(request):
    # 載入env
    dotenv.load_dotenv("./.env")

    # 初始化 webdriver
    driver = DriverFactory.create_driver("chrome")

    # 取得登入資訊
    company = os.getenv("COMPANY")
    user_name = os.getenv("ACCOUNT")
    password = os.getenv("PASSWORD")

    # 登入
    login_page = LoginPage(driver)
    res = login_page.login(company=company, username=user_name, password=password)

    if res:
        def end():
            quit_driver(driver)

        request.addfinalizer(end)

        return driver
    else:
        exit()