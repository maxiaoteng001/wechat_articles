# -*- coding: UTF-8 -*-
"""数据库转移"""
import traceback
from utils import crawler_utils
from utils import db_utils


def query_by_page(page_no=1, rows_no=10):
    """
    分页查询内容
    :param page_no:
    :param rows_no:
    :return:
    """
    limit_start = (page_no - 1) * rows_no
    limit_end = rows_no
    query_sql = 'select a.search_name AS search_name,a.article_title AS title,' \
                'a.article_abstract AS digest,a.article_wechat_name AS wechat_name,' \
                'a.article_url AS url,a.article_html AS article_html,NULL AS content,' \
                'a.article_timestamp AS article_timestamp,a.search_time AS search_time ' \
                'from wechat_article AS a' \
                ' limit {}, {}'.format(limit_start, limit_end)
    query_list = []
    try:
        db_connection = db_utils.get_connection()
        with db_connection.cursor() as cursor:
            cursor.execute(query_sql)
            results = cursor.fetchall()
            if results and len(results) > 0:
                for row in results:
                    query_list.append({
                        'search_name': row['search_name'],
                        'title': row['title'],
                        'digest': row['digest'],
                        'wechat_name': row['wechat_name'],
                        'url': row['url'],
                        'article_html': row['article_html'],
                        'content': '',
                        'article_timestamp': row['article_timestamp'],
                        'search_time': row['search_time']
                    })
        return query_list
    except Exception as e:
        traceback.print_exc()
        return query_list
    finally:
        return query_list


def __execute_article_insert(insert_values):
    """
    执行数据库插入
    :param insert_values:
    :return:
    """
    # search_name,title,digest,wechat_name,url,article_html,content,article_timestamp,search_time
    insert_sql = 'insert into wechat_article_v2 (search_name,title,digest,wechat_name,' \
                 'url,article_html,content,article_timestamp,search_time)' \
                 ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    db_utils.insert_many(insert_sql, insert_values)


if __name__ == '__main__':
    print('start')
    page_no = 1
    while True:
        print('page_no:{},rows_no:{}'.format(page_no, 1))
        article_list = query_by_page(page_no=page_no, rows_no=1)
        if len(article_list) == 0:
            break
        # search_name, title, digest, wechat_name, url, article_html, content, article_timestamp
        article_html = article_list[0]['article_html'].decode()
        content = crawler_utils.get_html_content(article_html)
        insert_values = [(article_list[0]['search_name'], article_list[0]['title'],
                          article_list[0]['digest'], article_list[0]['wechat_name'],
                          article_list[0]['url'], article_html, content,
                          article_list[0]['article_timestamp'],
                          article_list[0]['search_time'])]
        __execute_article_insert(insert_values)
        page_no += 1
        """
        if page_no > 10:
            break
        """

    print('success')
