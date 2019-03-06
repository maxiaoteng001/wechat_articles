from flask import Flask, request, jsonify
import os
import sys
from restfultools import * 

utils_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..')
sys.path.append(utils_dir)
from utils.mongodb_utils import get_db
from config_default import MONGODB_COLLECTION
db = get_db()
collection_name = MONGODB_COLLECTION

app = Flask(__name__)

datas = []

show_fields = [
    'title', 
    'digest',
    'url',
    'wechat_name',
    'search_name',
    'article_timestamp'
]


#获取所有的资源  注意我用了复数形式的url
@app.route('/articles')
def getAll():
    db_cursor = db.all_items(collection_name)
    for i in db_cursor:
        tmp_item = {}
        for field in show_fields:
            tmp_item[field] = i.get(field)
        datas.append(tmp_item)
    return fullResponse(R200_OK, datas)


#根据name获取资源中的某一个
@app.route('/article/<string:title>')
def getOne(title): 
    query = {
        "title": title
    }
    db_cursor = db.find(collection_name, query)
    # if len(db_cursor) == 0:
    #     return statusResponse(R404_NOTFOUND)
    for i in db_cursor:
        i.pop('_id')
        result = i
        break
    return fullResponse(R200_OK, result)
    

#POST请求，增加一项
@app.route('/article', methods=['POST'])
def addOne():
    request_data = request.get_json()
    if not 'name' in request_data or not 'useto' in request_data:
        return statusResponse(R400_BADREQUEST)
    name = request_data['name']
    useto = request_data['useto']
    datas.append({'name': name, 'useto': useto})
    return statusResponse(R201_CREATED)
    

#PUT，PATCH 更新资源
#按照RestFul设计：
#PUT动作要求客户端提供改变后的完整资源
#PATCH动作要求客户端可以只提供需要被改变的属性
#在这里统一使用PATCH的方法
@app.route('/article/<string:name>', methods=['PUT', 'PATCH'])
def editOne(name):
    result = [data for data in datas if data['name'] == name]
    if len(result) == 0:
        return statusResponse(R404_NOTFOUND)
    request_data = request.get_json()
    if 'name' in request_data:
        result[0]['name'] = request_data['name']
    if 'useto' in request_data:
        result[0]['useto'] = request_data['useto']
    return statusResponse(R201_CREATED)


#DELETE删除
@app.route('/article/<string:title>', methods=['DELETE'])
def delOne(title):
    query = {
        "title": title
    }
    db_cursor = db.remove(collection_name, query)
    if len(db_cursor) == 0:
        return statusResponse(R404_NOTFOUND)
    return statusResponse(R204_NOCONTENT)


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    # 项目入口
    app.config['JSON_AS_ASCII'] = False
    app.run(**config)