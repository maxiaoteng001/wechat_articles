# -*- coding: UTF-8 -*-
import logging
import config_default
import time
from utils import crawler_utils
from utils import log_utils
from utils import search_article_utils


def search_article(label_list, page_nos=[1]):
    """
    直接搜素文章
    :param label_list:待搜索的标签列表
    :param page_nos:待搜索的页面列表
    :return:
    """
    logging.info(u'===直接搜素文章开始：===')
    for page_no in page_nos:
        logging.info('第{}页开始'.format(page_no))
        for label in label_list:
            search_article_utils.search_wechat_article(label, page_no=page_no)
            crawler_utils.wait_sleep('两个标签爬取间隔', '')
    logging.info(u'===直接搜素文章结束！===')


if __name__ == '__main__':
    is_first = True
    while True:
        # 初始化日志配置
        file_handler, stream_handler = log_utils.log_init()
        config = config_default.configs
        wechat_list = config['wechat_list']
        logging.info(u'爬取任务开始：')
        # 待搜索的页码列表
        if is_first:
            page_no_list = config['first_page_no_list']
        else:
            page_no_list = config['page_no_list']

        is_first = False
        # 直接搜索文章
        search_article(wechat_list, page_no_list)
        logging.info(u'爬取任务结束！')
        next_turn_seconds = config['next_turn_seconds']
        logging.info(u'休息{}秒后进行下一轮爬取'.format(next_turn_seconds))
        time.sleep(next_turn_seconds)
        # 日志handler清除
        logging.getLogger().removeHandler(file_handler)
        logging.getLogger().removeHandler(stream_handler)
