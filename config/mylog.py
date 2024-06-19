# -*-coding:utf-8-*-
# @Time    : 2019/9/3 0003 15:15
# @Author  :zhu
# @File    : mylog.py
# @task description : 日志模块
import os
import sys
import logging
import logging.handlers
root_path = os.path.abspath(os.path.join(sys.path[0], '..'))
sys.path.append(root_path)
from config.set_config import Config_base


class LogMgr(object):
    def __init__(self, log_path: str, console_logger=False):
        self.logger = logging.getLogger(log_path)
        loghdlr = logging.handlers.TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=50000)
        self.fmt = logging.Formatter('%(asctime)s-%(levelname)s-%(lineno)d - %(message)s', '%Y-%m-%d %H:%M:%S')
        loghdlr.setFormatter(self.fmt)

        self.logger.addHandler(loghdlr)
        self.logger.parent.setLevel(logging.DEBUG)
        self.logger.setLevel(logging.INFO)

        """控制台输出"""
        if console_logger:
            self.set_console_logger()

    def set_console_logger(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(self.fmt)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger



