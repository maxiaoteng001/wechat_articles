"""搜索文章工具类"""
import logging
from utils import crawler_utils
from utils import db_utils
import os


def __get_search_url(search_name, page_no):
    """
    获取微信文章搜索url
    :param search_name:搜索内容
    :return:
    """
    if page_no > 1:
        search_url = 'http://weixin.sogou.com/weixin?query={}&_sug_type_=&s_from=input&_sug_=y&type=2&page=' \
                     + str(page_no) + '&ie=utf8'
    else:
        search_url = 'http://weixin.sogou.com/weixin?type=2&query={}&ie=utf8&s_from=input&_sug_=y&_sug_type_='
    return search_url.format(search_name)


def search_wechat_article(search_name, page_no=1):
    """
    搜索微信文章
    :param search_name: 搜索内容
    :param page_no: 页面
    :return:
    """
    origin_titles = crawler_utils.get_db_article_titles()
    search_url = __get_search_url(search_name, page_no)
    insert_values = __get_article_insert_values(search_name, search_url, origin_titles)
    if len(insert_values):
        logging.info(u'本次新增{}篇文章'.format(len(insert_values)))
        __execute_article_insert(insert_values)
    else:
        logging.info(u'本次没有文章更新')


def __execute_article_insert(insert_values):
    """
    执行数据库插入
    :param insert_values:
    :return:
    """
    # search_name,title,digest,wechat_name,url,article_html,content,article_timestamp,
    # article_rich_media
    insert_sql = 'insert into wechat_article (search_name,title,digest,wechat_name,' \
                 'url,article_html,content,article_timestamp,article_rich_media)' \
                 ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    db_utils.insert_many(insert_sql, insert_values)


def __get_article_insert_values(search_name, search_url, origin_titles):
    """获取文章待写入数据库的列表"""
    insert_values = []
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.text')
    data_dir = os.path.split(data_path)[0]
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    try:
        html_soup = crawler_utils.get_html_soup(search_url)
        if html_soup:
            ul_dom = html_soup.find("ul", class_="news-list")
            li_doms = ul_dom.find_all("li")
            for i in range(len(li_doms)):
                li_dom = li_doms[i]
                txt_box_dom = li_dom.find("div", class_="txt-box")
                titile_a_dom = txt_box_dom.find('h3').find('a')
                title = titile_a_dom.get_text("", strip=True)
                if title in origin_titles:  # 如果有该文章，则跳过
                    continue
                content_url = titile_a_dom['href']
                content_url = crawler_utils.format_wechat_url(content_url)
                txt_info_dom = li_dom.find("p", class_="txt-info")
                if txt_info_dom:
                    digest = txt_box_dom.get_text("", strip=True)
                else:
                    digest = ""
                txt_info_dom = li_dom.find("a", class_="account")
                if txt_info_dom:
                    wechat_name = txt_info_dom.get_text("", strip=True)
                else:
                    wechat_name = ""
                datetime_dom = li_dom.find("div", class_="s-p")
                if datetime_dom:
                    article_timestamp = datetime_dom['t']
                else:
                    article_timestamp = ""
                logging.info(u"微信公众号：{},标题：{}".format(wechat_name, title))
                article_html = crawler_utils.get_url_html_text(content_url)
                crawler_utils.wait_sleep('具体文章内容获取间隔休息', content_url)
                with open(data_path, 'r') as f:
                    count_data = f.read()
                    f.close()
                # 获取文章中的内容div
                article_rich_media = crawler_utils.get_js_article(article_html, count_data)
                # print(article_rich_media)
                if not article_rich_media:
                    continue
                # 获取文章内容
                article_text = crawler_utils.get_html_content(article_html)
                image_url = crawler_utils.get_image_url(article_html)
                insert_values.append((search_name, title, digest, wechat_name, content_url,
                                      article_html, article_text, article_timestamp,
                                      article_rich_media))
                data = int(count_data) + 1
                with open(data_path, 'w') as f:
                    s = str(data)
                    data = f.write(s)
                    f.close()

        else:
            crawler_utils.wait_sleep('标签搜索间隔休息', search_url)

        return insert_values
    except Exception as e:
        logging.error("异常信息:", e)
        logging.error('获取公众号文章失败')
        return insert_values
