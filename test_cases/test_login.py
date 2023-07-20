# import pytest
# from page_object.login_page import LoginPage
# from page_object.home_page import HomePage

# # 登入測試
# class Test_login():
#     @pytest.mark.dependency()
#     def test_login(self, login_page):
#         home_page = HomePage(login_page.driver)
#         home_page.go_home()
#         assert login_page.driver.title == "NUEiP - 總覽"

# if __name__ == '__main__':
#     pytest.main(['-v', 'test_login.py'])