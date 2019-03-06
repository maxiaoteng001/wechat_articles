# -*- coding: UTF-8 -*-
"""爬虫工具类"""
import logging
import random
import re
import os
import sys
import time
from urllib import request
import requests
from bs4 import BeautifulSoup
from .abuyun import get_proxies
from utils import db_utils
from .mongodb_utils import get_db

cwdpath = sys.path[0]

verify_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..')
sys.path.append(verify_dir)
from verification_code import ydm_verify_code 


def get_url_html_text(url):
    """
    获取url的html文件
    :param url: url地址
    :return:
    """
    try:
        headers = {
            'User-Agent': random.choice(__user_agents)
        }
        html = requests.get(url, headers=headers, proxies=get_proxies())  # , proxies=proxies
        html.encoding = 'utf-8'  # 这一行是将编码转为utf-8否则中文会显示乱码。
        return html.text
    except Exception as e:
        logging.error("异常信息:{}".format(e))
        logging.error('请求错误,url为:{}'.format(url))
        return None


# 代理
__user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


def get_html_soup(url):
    """
    根据url获取html的soup
    :param url:
    :return:
    """
    for i in range(1, 4):  # 出现验证码会执行三次
        html_dom = get_url_html_text(url)
        wait_sleep('soup获取间隔休息', url)
        if not html_dom:
            return None
        html_soup = BeautifulSoup(html_dom, "html.parser")
        title_dom = html_soup.find('title')
        if title_dom:
            title_text = title_dom.get_text("", strip=True)
            if "验证码" in title_text or '"请输入验证码"' in str(html_soup):
                logging.warning('第{}次尝试，出现验证码'.format(i))
                # 请求一个新的验证码并验证
                ydm_verify_code.input_code_by_url(url)
                wait_sleep('搜索出现验证码休息', url, verify_code=True)
                continue
                # break
            else:
                return html_soup
        else:
            return html_soup

    return None


def format_wechat_url(url):
    """
    格式化微信搜索地址的url，去掉amp;
    :param url:待格式化的url
    :return:格式化后的url
    """
    return re.sub(r'amp;', "", url)


def wait_sleep(content, url, verify_code=False):
    """
    睡眠等待
    :param content:描述
    :param url:出现验证码的地址
    :param verify_code:是否出现验证码
    :return:
    """
    if verify_code:  # 出现验证码程序休眠秒数        
        seconds = random.randint(50, 70)
    else: # 一般网页查询程序休眠秒数
        seconds = random.randint(50, 70)
    logging.warning(u'{}，睡眠{}秒'.format(content, seconds))
    logging.warning(url)
    time.sleep(seconds)


def log_init():
    """配置日志信息"""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        filename=cwdpath + '/log/log_{}.txt'.format(time.strftime("%Y%m%d_%H%M%S", time.localtime())),
                        filemode='w')
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # 设置日志打印格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('').addHandler(console_handler)
    return console_handler


def get_html_content(html_str):
    """
    获取html内的文本内容（body标签内所有文本内容）
    :param html_str:html串
    :return:文本内容
    """
    html_soup = BeautifulSoup(html_str, "html.parser")
    body_dom = html_soup.find('body')
    [s.extract() for s in body_dom('script')]  # 删除页面script标签
    #print(body_dom)
    return body_dom.get_text("", strip=True)


def get_js_article(html_str, content_time):
    """
    获取js_article
    :param html_str:
    :return:
    """
    #save_image(html_str, content_time)
    try:
        html_soup = BeautifulSoup(html_str, "html.parser")
        save_images(html_str, content_time)
        js_article = html_soup.select("p")
        res = ''
        for i in js_article[1:-6]:
            res = res + str(i)

        soup = BeautifulSoup(res, 'html.parser')
        article_rich_media = ''
        number = 0
        for i in soup:
            s = i.text
            if s:
                case = '<p>' + s + '</p>'
            else:
                case = ''
            if 'align' or 'img' in i:
                img = i.select('img')
                if img:  
                    # ['data-src']
                    # img_url = img[0]['data-src']
                    # 12/21 修改, 图片添加loading_url
                    loading_url = 'http://static.wechat.maxiaoteng.tk/app/default/loading.gif'
                    img_url = 'http://static.wechat.maxiaoteng.tk/news/{}/{}.png'.format(content_time, number)
                    onerror_str = "javascript:this.style.display='none'"
                    mg1 = '<img style="max-width: 100% !important; height: auto !important; visibility: visible !important;" src="{}" data-src="{}" onerror="{}">'.format(img_url, img_url, onerror_str)
                    mg = '<p style="text-align: center">' + mg1 + '</p>' + '\n'
                    number += 1
                else:
                    mg = ''
            else:
                mg = ''

            article_rich_media = article_rich_media + case + mg
        # 12/21 新加js代码配合loading_url, 图片加载时展示加载图片
        timeout_js = """
        <script>
            setTimeout(function () {
                var imgs = document.querySelectorAll("img");
                for (i = 0; i < imgs.length; i++) {
                    var src = imgs[i].getAttribute("data-src");
                    if (src) {
                        imgs[i].setAttribute("src", src)
                    }
                }
            },800)
        </script>
        """
        article_rich_media += timeout_js
        return article_rich_media
    except Exception as e:
        logging.error('获取js_article错误：', e)
        return None

def get_image_url(html_str):
    try:
        html_soup = BeautifulSoup(html_str, "html.parser")
        js_article = html_soup.select("p")
        image_url_list = ''
        j = 0
        for i in js_article[1:-8]:
            image = i.select('img')
            j += 1
            if image:
                image_url = image[0]['data-src']
                image_url_list = image_url_list + image_url + ' '

        return image_url_list
    except Exception as e:
        logging.error('获取image_url错误：', e)
        return None

def save_images(html, content_time):
    try:
        html_soup = BeautifulSoup(html, "html.parser")
        try:
            two_image = html_soup.select('section > img')[0]['data-src']
        except:
            two_image = None
        image_lists = html_soup.select('img')
        path = '/root/www/sddl/tech/storage/news/{}'.format(content_time)
        #print(path)
        if not os.path.exists(path):
            os.makedirs(path)
        image_list = []
        for x in image_lists:
            try:
                image = x['data-src']
                if image == two_image:
                    pass
                else:
                    image_list.append(image)
                #image_list.append(image)
            except:
                pass
        i = 0
        for image_url in image_list:
            response = requests.get(image_url, proxies=get_proxies())
            cat_img = response.content
            image_path = path + '/{}.png'.format(i)
            with open(image_path, 'wb') as f:
                f.write(cat_img)
                f.close()
            i += 1

    except Exception as e:
        print(e)


def get_db_article_titles():
    """
    获取数据库中已有的文章标题列表
    :return:
    """
    # query_sql = 'SELECT title FROM wechat_article'
    # titles = []
    # try:
    #     db_connection = db_utils.get_connection()
    #     with db_connection.cursor() as cursor:
    #         cursor.execute(query_sql)
    #         results = cursor.fetchall()
    #         if results and len(results) > 0:
    #             for row in results:
    #                 titles.append(row['title'])
    #     return titles
    # except Exception as e:
    #     logging.error("异常信息:", e)
    # finally:
    #     db_connection.close()

    # 改用mongodb
    titles = []
    db = get_db()
    collection_name = 'wechat'
    all_items = db.find(collection_name)
    for item in all_items:
        titles.append(item.get('title'))
    return titles


def get_today_date():
    value = time.localtime(time.time())
    format = '%Y-%m-%d'
    dt = time.strftime(format, value)
    return dt

