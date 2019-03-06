import pymysql
from config_default import configs


def get_wechat_name():
    # config = {
    #     'host':'47.98.116.79',
    #     'port': 3306,
    #     'user': 'root',
    #     'passwd': 'newtech123',
    #     'db': 'newtech',
    #     'charset': 'utf8'
    #     }
    #
    # conn = pymysql.connect(**config)
    #
    # cursor = conn.cursor()
    # cursor.execute('SELECT name, account FROM wechat_name')
    # results = cursor.fetchall()
    # conn.close()
    results = configs.get('weixinhao')
    return results