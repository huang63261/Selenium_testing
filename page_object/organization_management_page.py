from base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WD
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

class OrganizationManagement(BasePage):
    url = "/organization_management"

    """存取控件 & 元素操作"""
    # 新增按鈕
    add_btn = (By.ID, "main_add")
    # 名稱
    d_name = (By.ID, "d_name")
    # 上層部門下拉選單
    parent_dept = (By.XPATH, '//*[@id="main_content"]//button[@data-id="dept_no"]')
    # 上層部門搜尋框
    parent_dept_search = (By.XPATH, '//div[@class="bs-searchbox"]/input[@aria-label="Search"]')
    # 上層部門下拉選單選項
    parent_dept_options = (By.CLASS_NAME, "dropdown-item")
    # 部門層級下拉選單
    d_level = (By.ID, "d_level")
    # 部門主管多選選單
    manager_company_option = (By.ID, "company_option")
    manager_dept_main = (By.ID, "dept_main")
    # 簽核副本通知 Radio (0.否/ 1.主管請假時才發送/ 2.一律發送)
    send_cc_option0 = (By.ID, "send_cc_0")
    send_cc_option1 = (By.ID, "send_cc_1")
    send_cc_option2 = (By.ID, "send_cc_2")
    # 生效日期
    s_date = (By.ID, "s_date")
    # 備註
    remark = (By.ID, "remark")
    # 錯誤訊息
    error_message = (By.ID, "error_message")
    # 返回
    modalBack = (By.ID, "ModalBack")
    # 儲存
    modalSave = (By.NAME, "ModalSave")
    # 部門資料 table
    table_content = (By.ID, "table_content")
    table_content_rows = (By.XPATH, '//*[@id="table_content"]/tbody/tr')
    # 排班可用班別/地點
    shift_tab = (By.XPATH, '//*[@id="shift"]/a[@data-value="shift"]')
    # 班表管理 URL
    class_management = (By.XPATH, '//*[@id="main_content"]//a[@href="/hr_class_management"]')
    # 可選班別
    class_list = (By.ID, "classList")
    # 已選班別
    class_selected = (By.ID, "selected")
    # 排班可用地點
    location_list = (By.ID, "location-list")
    # 已選地點
    location_selected = (By.ID, "selected-location")

    def __init__(self, driver, timeout=3) -> None:
        super().__init__(driver, timeout)
        # 存放部門資料
        self.dept_table = {}
        # 存放部門名稱
        self.dept_name = []

    # 取得部門列表中 所有DOM元件與名稱
    def get_all_departments(self):
        # 資料清除
        self.dept_table.clear()
        self.dept_name.clear()

        # 強行等待 0.5s，等待AJAX載入完全
        self.sleep(0.5)

        rows = WD(self.driver, 5).until(lambda x: x.find_elements(*self.table_content_rows))

        for row in rows:
            colums = row.find_elements(By.XPATH, "./td")
            self.dept_table[colums[3].text] = {
                "edit": colums[0].find_element(By.XPATH, "./i"),
                "delete": colums[1].find_element(By.XPATH, "./i"),
                "abolish": colums[2].find_element(By.XPATH, "./i"),
                "dept_name": colums[3].text,
                "level": colums[4].text,
                "subsitute_manager": colums[5].find_element(By.XPATH, "./span"),
                "members": colums[6].find_element(By.XPATH, "./span"),
                "status": colums[7]
            }

        # 儲存部門名稱列表
        self.dept_name = list(self.dept_table.keys())

        return self.dept_table

    # 新增部門
    def add_dept(self):
        try:
            # 開啟部門管理
            self.open_url(self.url)

            # 點擊新增按鈕
            self.click(*self.add_btn)

            # 是否順利進入新增頁面
            if (self.get_current_url() == self.base_url + self.url + "/active"):
                # 新增時間
                now = str(time.time())
                dept_name = "add_testing_" + now
                # 填入部門名稱
                self.send_keys(*self.d_name, dept_name)

                # 點擊上層部門下拉選單
                self.click(*self.parent_dept)
                # 點選上層部門
                parent_dept_options = self.find_elements(*self.parent_dept_options)
                parent_dept_options[1].click()

                # 部門層級
                d_level = self.get_select(*self.d_level)
                # 透過select index 選擇 【部】
                d_level.select_by_index('4')

                # 部門主管
                # manager_company_option = self.get_select(*self.manager_company_option)
                manager_dept_main = self.get_select(*self.manager_dept_main)
                manager_dept_main.select_by_index('0')

                # 簽核副本通知
                self.click(*self.send_cc_option1)

                # 生效日期
                self.select_date_picker(*self.s_date, "2023-01-01")

                # 填入備註
                self.send_keys(*self.remark, "自動化測試-新增")

                # 點擊儲存
                self.click(*self.modalSave)

                # 取得部門列表物件
                self.get_all_departments()

                assert dept_name in self.dept_name
            else:
                raise Exception("[Test][Fail]Incorrect URL")

        except Exception as E:
            self.log_error(str(E))
            assert False

    # 編輯部門
    def edit_dept(self, key=0):
        try:
            # 開啟部門管理
            self.open_url(self.url)

            # 取得部門列表物件
            self.get_all_departments()

            # 編輯時間
            now = str(time.time())

            # 點擊修改
            self.dept_table[self.dept_name[key]]["edit"].click()

            # 部門名稱
            dept_name = "edit_testing_" + now

            # 修改部門名稱
            self.send_keys(*self.d_name, dept_name)

            # 點擊上層部門下拉選單
            self.click(*self.parent_dept)
            # 選擇上層部門 (透過搜尋框輸入)
            parent_dept_search = self.find_element(*self.parent_dept_search)
            parent_dept_search.send_keys("HarveyHuangTest")
            parent_dept_search.send_keys(Keys.ENTER)

            # 簽核副本通知
            self.click(*self.send_cc_option0)

            # 生效日期
            self.select_date_picker(*self.s_date, "2023-07-01")

            # 填入備註
            self.send_keys(*self.remark, "自動化測試-編輯")

            # 點擊 排班可用班別/地點 頁籤
            shift_tab = self.find_element(*self.shift_tab)
            # 使用element.click()會因為視窗遭遮住無法順利點擊，使用execute_script執行JS代替
            self.driver.execute_script("arguments[0].click();", shift_tab)

            # 已選地點 (逐一取消選取)
            location_selected = self.get_select(*self.location_selected)
            location_selected_options = location_selected.options
            for option in location_selected_options:
                option.click()

            # 排班可用地點 (選取ALL)
            location_list = self.get_select(*self.location_list)
            location_list.select_by_visible_text("總店")
            location_list.select_by_visible_text("分店")

            # 點擊儲存
            self.click(*self.modalSave)
        except Exception as E:
            self.log_error(str(E))
            assert False

        # 成功返回部門管理頁
        if self.get_current_url() == self.base_url + self.url:
            # 重新取得部門列表物件
            self.get_all_departments()
            # 檢查是否編輯成功
            assert dept_name in self.dept_name
        else:
            # 取得錯誤訊息
            error_message = self.find_element(*self.error_message)
            # 寫入Log
            self.log_error(error_message.txt)
            assert False

    # 刪除部門
    def delete_dept(self, key=0):
        # 開啟部門管理
        self.open_url(self.url)

        # 取得部門列表物件
        self.get_all_departments()

        # 是否可刪除
        deletable_flag = self.dept_table[self.dept_name[key]]["delete"].get_attribute("class").find("disabled") == -1

        if deletable_flag:
            dept_name = self.dept_name[key]
            # 點擊刪除
            self.dept_table[dept_name]["delete"].click()
            # 強行等待 0.5s
            self.sleep(0.5)
            # 取得彈窗相依編號
            popover_id = self.dept_table[self.dept_name[key]]["delete"].get_attribute("aria-describedby")
            # 刪除彈窗定位
            popover = self.find_element(By.ID, popover_id)
            # 【是】按鈕定位
            confirm_btn = popover.find_element(By.XPATH, "//div[@class='popover-content']//input[@data-answer='yes']")
            # 確認刪除
            confirm_btn.click()

            # 重新抓取部門table
            self.get_all_departments()

            assert dept_name not in self.dept_name
        else:
            self.log_error("該部門無法刪除")
            assert False

    # # 裁撤部門
    def abolish_dept(self, key=0):
        return

    # # 編輯主管
    def edit_manager(self, key=0):
        return

    # # 編輯代理主管
    def edit_subsitute_manager(self, key=0):
        return