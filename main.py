# -*- coding: UTF-8 -*-
import logging
import config_default
import time
from utils import crawler_utils
from utils import log_utils
from utils import search_weixinhao_utils
from get_article_list import get_wechat_name

def search_article(weixinhaos):
    """
    微信号爬取
    :param weixinhaos:微信号列表
    :param page_nos:待搜索的页面列表
    1
    2
    3
    :return:
    """
    for weixinhao, account_name in weixinhaos:
        logging.info('weixinhao：{},account_name:{} 开始'.format(weixinhao, account_name))
        weixinhao_url, account_name = search_weixinhao_utils.get_weixinhao_url(weixinhao)
        if weixinhao_url:
            search_weixinhao_utils.save_wechat_article(weixinhao_url, weixinhao, account_name)
        else:
            logging.error('weixinhao：{}失效'.format(weixinhao))
        crawler_utils.wait_sleep('两个微信号爬取间隔', '')

if __name__ == '__main__':
    is_first = True
    while True:
        # 初始化日志配置
        file_handler, stream_handler = log_utils.log_init()
        config = config_default.configs
        weixinhao_list = config['weixinhao']
        logging.info(u'爬取任务开始：')
        # 搜索公众号
        weixinhao_list = get_wechat_name()
        search_article(weixinhao_list)
        logging.info(u'爬取任务结束！')
        next_turn_seconds = config['next_turn_seconds']
        logging.info(u'休息{}秒后进行下一轮爬取'.format(next_turn_seconds))
        # time.sleep(next_turn_seconds)
        # 日志handler清除
        logging.getLogger().removeHandler(file_handler)
        logging.getLogger().removeHandler(stream_handler)

        # break, 用定时任务重启
        break