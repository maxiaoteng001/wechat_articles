# -*- coding: UTF-8 -*-
import logging
import sys
import time

cwdpath = sys.path[0]


def log_init():
    """配置日志信息"""
    # 创建一个handler，用于写入日志文件
    logging.basicConfig(level=logging.INFO)  # 设置日志级别
    file_name = cwdpath + '/log/log_{}.log'.format(time.strftime("%Y%m%d_%H%M%S", time.localtime()))
    file_handler = logging.FileHandler(filename=file_name, mode='w', encoding='utf-8')
    # file_handler.setLevel(logging.INFO)

    # 再创建一个handler，用于输出到控制台
    stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(logging.INFO)

    # 定义handler的输出格式formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # 给logger添加handler
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().addHandler(stream_handler)
    return file_handler, stream_handler
