# -*- coding: UTF-8 -*-
import logging
import time
from utils import log_utils

if __name__ == '__main__':
    # 初始化日志配置
    file_handler, stream_handler = log_utils.log_init()
    logging.info(u'info你好啊！')
    logging.warning(u'warn你好啊！')
    logging.error(u'error你好啊！')
    logging.debug(u'debug你好啊！')
    # 日志handler清除
    logging.getLogger().removeHandler(file_handler)
    logging.getLogger().removeHandler(stream_handler)
    time.sleep(5)
