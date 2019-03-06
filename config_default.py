# -*- coding: UTF-8 -*-
# 默认配置
configs = {
    'next_turn_seconds': 36000,  # 运行整个轮次结束后休息多少秒
    'db': {  # 数据库连接配置
        'host': 'localhost',
        'user': 'root',
        'password': 'j_81wLei4HFLY0VR',
        'db_name': 'wechat',
        'charset': 'utf8mb4'
    },
    'weixinhao': (  # 待爬取公众号类型列表
        ('gh_3d8809822dc1', '鱼眼看电改'),
        ('FViewXFG', '爱否科技'),
        ('almosthuman2014', '机器之心'),
        ('svblock', '硅谷区块链'),
        ('qklsdgc', '区块链深度观察'),
        ('mit-tr', 'DeepTech深科技'),
        ('aitechtalk', 'AI科技评论'),
        ('OKBlockchain', 'OK区块链'),
        ('openstackcn', '开源云中文社区'),
        ('ali_tech', '阿里技术'),
        ('ai-front', 'AI前线'),
    )
}


# 数据库配置
# MONGODB_SERVER = 'localhost'
# MONGODB_PORT = 27017
# USER = 'maxiaoteng'
# PASSWORD = 'yunfutech'
# MONGODB_DATABASE = 'dianping'
# MONGODB_COLLECTION = ''


# 数据库配置
MONGODB_SERVER = '13.57.255.239'
MONGODB_PORT = 27017
USER = 'maxiaoteng'
PASSWORD = 'maxiaoteng'
MONGODB_DATABASE = 'first'
MONGODB_COLLECTION = ''
