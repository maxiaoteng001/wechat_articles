# -*- coding: UTF-8 -*-
"""数据库工具类"""
import pymysql
import logging
import config_default


def get_connection():
    """mysql数据库连接"""
    config = config_default.configs
    connection = pymysql.connect(
        host=config['db']['host'],
        user=config['db']['user'],
        password=config['db']['password'],
        db=config['db']['db_name'],
        charset=config['db']['charset'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def insert_many(insert_sql, insert_values):
    """
    数据库插入多条
    :param insert_sql:插入语句
    :param insert_values:待插入的list
    :return:
    """
    try:
        db_connection = get_connection()
        with db_connection.cursor() as cursor:
            cursor.executemany(insert_sql, insert_values)
            db_connection.commit()
    except Exception as e:
        logging.error("异常信息:", e)
        raise Exception('数据库插入多条异常')
    finally:
        db_connection.close()


def execute(execute_sql, args):
    """
    执行数据库语句
    :param execute_sql:数据库语句
    :return:
    """
    try:
        db_connection = get_connection()
        with db_connection.cursor() as cursor:
            cursor.execute(execute_sql, args)
            db_connection.commit()
    except Exception as e:
        logging.error("异常信息:", e)
        raise Exception('数据库操作异常')
    finally:
        db_connection.close()
