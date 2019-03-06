# -*- coding: UTF-8 -*-
"""数据库转移"""
import traceback

from bs4 import BeautifulSoup

from utils import db_utils
from utils import crawler_utils


def query_by_page(page_no=1, rows_no=10):
    """
    分页查询内容
    :param page_no:
    :param rows_no:
    :return:
    """
    limit_start = (page_no - 1) * rows_no
    limit_end = rows_no
    query_sql = 'select a.id AS id,a.article_html AS article_html ' \
                'from wechat_article AS a WHERE a.article_rich_media IS NULL ' \
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
                        'id': row['id'],
                        'article_html': row['article_html']
                    })
        return query_list
    except Exception as e:
        traceback.print_exc()
        return query_list
    finally:
        return query_list


if __name__ == '__main__':
    print('start')
    page_no = 1
    while True:
        print('page_no:{},rows_no:{}'.format(page_no, 1))
        article_list = query_by_page(page_no=page_no, rows_no=1)
        if len(article_list) == 0:
            break
        # id, article_html
        article_html = article_list[0]['article_html']
        article_id = article_list[0]['id']
        article_rich_media = crawler_utils.get_js_article(article_html)
        if not article_rich_media:
            article_rich_media = ''
        execute_sql = 'UPDATE wechat_article SET article_rich_media = %s ' \
                      'WHERE id = %s'
        db_utils.execute(execute_sql, (str(article_rich_media), str(article_id)))
        page_no += 1
        """
        if page_no > 10:
            break
        """

    print('success')
