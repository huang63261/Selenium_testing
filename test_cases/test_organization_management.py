import pytest
from page_object.organization_management_page import OrganizationManagement

@pytest.fixture
def om_page(driver):
    om_page = OrganizationManagement(driver)
    yield om_page

# 部門管理測試頁面
class Test_organization_management():
    # 新增部門測試
    # @pytest.mark.skip(reason="測試案例跳過")
    def test_add_dept(self, om_page):
        om_page.add_dept()

    # 編輯部門測試
    @pytest.mark.skip(reason="測試案例跳過")
    def test_edit_dept(self, om_page):
        om_page.edit_dept()

    # 刪除部門測試
    @pytest.mark.skip(reason="測試案例跳過")
    def test_delete_dept(self, om_page):
        om_page.delete_dept()

if __name__ == '__main__':
    pytest.main(['-v', 'test_organization_management.py'])