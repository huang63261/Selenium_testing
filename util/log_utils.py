import time
import os
import logging

currrent_path = os.path.dirname(__file__)
log_path = os.path.join(currrent_path, '../logs')

class LogUtils:
    def __init__(self, log_path=log_path):
        """
        通過Python自帶的logging模組進行封裝
        """
        self.logfile_path = log_path
        # 創建日誌對象logger
        self.logger = logging.getLogger(__name__)
        # 設置日誌級別
        self.logger.setLevel(level=logging.INFO)
        # 設置日誌的格式
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        """在log檔中輸出日誌"""
        # 日誌檔案名稱顯示一天的日誌
        self.log_name_path = os.path.join(self.logfile_path, "log_%s" % time.strftime('%Y_%m_%d')+".log")
        # 創建文件處理程序並實現追加
        self.file_log = logging.FileHandler(self.log_name_path, 'a', encoding='utf-8')
        # 設置日誌檔中的格式
        self.file_log.setFormatter(formatter)
        # 設置日誌檔中的級別
        self.file_log.setLevel(logging.INFO)
        # 把日誌訊息輸出到文件中
        self.logger.addHandler(self.file_log)
        # 關閉文件
        self.file_log.close()

        """在控制台輸出日誌"""
        # 日誌在控制台
        # self.console = logging.StreamHandler()
        # # 設置日誌級別
        # self.console.setLevel(logging.INFO)
        # # 設置日誌格式
        # self.console.setFormatter(formatter)
        # # 把日誌訊息輸出到控制台
        # self.logger.addHandler(self.console)
        # # 關閉控制台日誌
        # self.console.close()

    def get_log(self):
        return self.logger


if __name__ == '__main__':
    logger = LogUtils().get_log()

    logger.info('123')
    logger.error('error')