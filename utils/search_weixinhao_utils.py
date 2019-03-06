"""微信公众号帐号获取"""
import json
import logging
import re
import sys
import os
from utils import crawler_utils
from utils import db_utils
import requests
cwdpath = sys.path[0]
from .abuyun import get_proxies


def __get_search_url(weixinhao):
    """
    获取微信公众号搜索url
    :param weixinhao:待搜索的微信号
    :return:
    """
    url = 'http://weixin.sogou.com/weixin?type=1&query={}&ie=utf8&s_from=input&_sug_=y&_sug_type_='
    return url.format(weixinhao)


def get_weixinhao_url(weixinhao):
    """
    获取微信公众号地址
    :param weixinhao: 待搜索的微信号
    :return:
    """
    weixinhao_url = None
    account_name = None
    try:
        url = __get_search_url(weixinhao)
        html_soup = crawler_utils.get_html_soup(url)
        if html_soup:
            ul_dom = html_soup.find("ul", class_="news-list2")
            tit_dom = ul_dom.find("p", class_="tit")
            if tit_dom:
                account_dom = tit_dom.find('a')
                account_href = account_dom['href']
                account_name = account_dom.get_text("", strip=True)
                weixinhao_url = crawler_utils.format_wechat_url(account_href)
        else:
            crawler_utils.wait_sleep('标签搜索间隔休息', url)
        return weixinhao_url, account_name
    except Exception as e:
        logging.error('获取微信公众号地址失败:', e)
        return weixinhao_url, account_name


def save_wechat_article(weixinhao_url, weixinhao, account_name):
    """
    保存微信公众号文章
    :param weixinhao_url:微信公众号地址
    :param weixinhao:微信号
    :param account_name:微信号中文名
    :return:
    """
    try:
        origin_titles = crawler_utils.get_db_article_titles()
        msg_list = __get_msg_list(weixinhao_url)
        if msg_list:
            insert_values = __get_article_insert_values(msg_list, account_name, weixinhao, origin_titles)
            if len(insert_values):
                __execute_article_insert(insert_values)
                logging.info(u'本次新增{}篇文章'.format(len(insert_values)))
            else:
                logging.info(u'本次没有文章更新')
        else:
            logging.warning(u'该公众号没有爬取到结果')
    except Exception as e:
        logging.error('异常信息:', e)
        logging.error(u'搜索公众号:{}出现错误'.format(weixinhao))


def __execute_article_insert(insert_values):
    """
    执行数据库插入
    :param insert_values:
    :return:
    """
    # search_name,title,digest,wechat_name,url,article_html,content,article_timestamp,
    # article_rich_media
    insert_sql = 'insert into wechat_article (search_name,title,digest,wechat_name,' \
                 'url,article_html,content,article_timestamp,article_rich_media, cover)' \
                 ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    db_utils.insert_many(insert_sql, insert_values)


def __get_msg_list(url):
    """
    获取公众号内的文章列表json
    :param url:公众号url
    :return:
    """
    html_soup = crawler_utils.get_html_soup(url)
    msg_list = None
    if html_soup:
        pattern = re.compile(r"var msgList = (.*?);$", re.MULTILINE | re.DOTALL)
        script = html_soup.find("script", text=pattern)
        msg_list_str = pattern.search(script.text).group(1)
        logging.debug(u'msgList:{}'.format(msg_list_str))
        msg_list = json.loads(msg_list_str)
        #print(html_soup)
    else:
        crawler_utils.wait_sleep('公众号文章列表获取间隔休息', url)
    return msg_list

def save_image(data, cover_url):
    try:
        path = '/root/www/sddl/tech/storage/news/{}'.format(data)
        #print(path)
        if not os.path.exists(path):
            os.makedirs(path)
        response = requests.get(cover_url, proxies=get_proxies())
        cat_img = response.content
        image_path = path + '/01.png'
        with open(image_path, 'wb') as f:
            f.write(cat_img)
            f.close()

    except Exception as e:
        return None

def __get_article_insert_values(msg_list, wechat_name, label, origin_titles):
    """
    获取数据插入列表
    :param msg_list:
    :param wechat_name:
    :param label:
    :param origin_titles:
    :return:
    """
    # data_path = 'C:/Users/Administrator/Desktop/wechat_articles/utils/data.text'
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.text')
    data_dir = os.path.split(data_path)[0]
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    insert_values = []
    url_prefix = 'https://mp.weixin.qq.com'
    article_list = msg_list['list']
    for article_temp in article_list:
        app_msg_ext_info = article_temp['app_msg_ext_info']
        comm_msg_info = article_temp['comm_msg_info']

        article_timestamp = comm_msg_info['datetime']  # 文章时间戳

        multi_app_msg_item_list = app_msg_ext_info['multi_app_msg_item_list']
        # 一次推送，多个内容
        if multi_app_msg_item_list and len(multi_app_msg_item_list) > 0:
            for multi_app_msg_item in multi_app_msg_item_list:
                cover = multi_app_msg_item['cover']
                with open(data_path, 'r') as f:
                    data1 = f.read()
                    f.close()
                save_image(data1, cover_url=cover)
                cover_1 = 'http://static.sddl.yunfutech.com/news/{}/01.png'.format(data1)
                title = multi_app_msg_item['title']  # 标题
                if title in origin_titles:  # 如果有该文章，则跳过
                    continue
                digest = multi_app_msg_item['digest']  # 摘要
                # author = multi_app_msg_item['author']  # 作者
                content_url = url_prefix + multi_app_msg_item['content_url']  # 文章地址
                content_url = crawler_utils.format_wechat_url(content_url)
                # source_url = multi_app_msg_item['source_url']  # 源地址

                article_html = crawler_utils.get_url_html_text(content_url)
                crawler_utils.wait_sleep('具体文章内容获取间隔休息', content_url)
                if not article_html:
                    continue
                # 获取文章中的内容div
                with open(data_path, 'r') as f:
                    count_data = f.read()
                    f.close()
                article_rich_media = crawler_utils.get_js_article(article_html, count_data)
                if not article_rich_media:
                    continue
                # 获取文章内容
                article_text = crawler_utils.get_html_content(article_html)
                if len(article_text) < 10:
                    continue

                insert_values.append((label, title, digest, wechat_name, content_url,
                                      article_html, article_text, article_timestamp,
                                      article_rich_media, cover_1))
                data2 = int(count_data) + 1
                with open(data_path, 'w') as f:
                    s = str(data2)
                    data = f.write(s)
                    f.close()


        else:
            cover = app_msg_ext_info['cover']
            with open(data_path, 'r') as f:
                data1 = f.read()
                f.close()
            save_image(data1, cover_url=cover)
            cover_1 = 'http://static.sddl.yunfutech.com/news/{}/01.png'.format(data1)
            with open(data_path, 'r') as f:
                count_data = f.read()
                f.close()
            # 一次推送，一片文章
            title = app_msg_ext_info['title']  # 标题
            if title in origin_titles:  # 如果有该文章，则跳过
                continue
            digest = app_msg_ext_info['digest']  # 摘要
            # author = app_msg_ext_info['author']  # 作者
            content_url = url_prefix + app_msg_ext_info['content_url']  # 文章地址
            content_url = crawler_utils.format_wechat_url(content_url)
            # source_url = app_msg_ext_info['source_url']  # 源地址
            article_html = crawler_utils.get_url_html_text(content_url)
            crawler_utils.wait_sleep('具体文章内容获取间隔休息', content_url)
            if not article_html:
                continue
            # 获取文章中的内容div
            article_rich_media = crawler_utils.get_js_article(article_html, count_data)
            if not article_rich_media:
                continue
            # 获取文章内容
            article_text = crawler_utils.get_html_content(article_html)
            if len(article_text) < 10:
                continue
            insert_values.append((label, title, digest, wechat_name, content_url,
                                  article_html, article_text, article_timestamp,
                                  article_rich_media, cover_1))
            data = int(count_data) + 1
            with open(data_path, 'w') as f:
                s = str(data)
                data = f.write(s)
                f.close()
    return insert_values
    #return None
