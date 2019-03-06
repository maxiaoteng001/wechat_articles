import http.client, mimetypes, urllib, json, time, requests
import requests
import random
import time
import os
import sys
utils_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..')
sys.path.append(utils_dir)
from utils import crawler_utils

######################################################################

class YDMHttp:

    apiurl = 'http://api.yundama.com/api.php'
    username = ''
    password = ''
    appid = ''
    appkey = ''

    def __init__(self, username, password, appid, appkey):
        self.username = username  
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        response = self.post_url(self.apiurl, fields, files)
        response = json.loads(response)
        return response
    
    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001
    
    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    def report(self, cid):
        data = {'method': 'report', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'cid': str(cid), 'flag': '0'}
        response = self.request(data)
        if (response):
            return response['ret']
        else:
            return -9001

    def post_url(self, url, fields, files=[]):
        for key in files:
            files[key] = open(files[key], 'rb');
        res = requests.post(url, files=files, data=fields)
        return res.text

######################################################################

# 用户名
username    = 'yunfutech'

# 密码
password    = 'Lcbb49r9iZWhkBF'                            

# 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
appid       = 1                                     

# 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
appkey      = '22cc5376925e9387a23cf797cb9ba745'    

# 图片文件
filename    = ''                        

# 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
codetype    = 1004

# 超时时间，秒
timeout     = 60                                    


def demo(): 
    # 检查
    if (username == 'username'):
        print('请设置好相关参数再测试')
    else:
        # 初始化
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login();
        print('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance();
        print('balance: %s' % balance)

        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, codetype, timeout);
        print('cid: %s, result: %s' % (cid, result))

    ######################################################################

def get_verify_code(filename):
    # 图片文件
    # filename    = 'verifycode.png'

    if (username == 'username'):
        print('请设置好相关参数再测试')
    else:
        # 初始化
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login();
        print('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance();
        print('balance: %s' % balance)

        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, codetype, timeout);
        print('cid: %s, result: %s' % (cid, result))

        return result


def save_verify_image(url):
    '''
    根据url下载验证码图片,按照日期建立文件夹,文件名为url的最后一节,后缀名png
    '''
    today = crawler_utils.get_today_date()
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../verify_pics/{}'.format(today))
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    cert = url.split('=')[-1]
    image_name = url.split('=')[-1].replace('.', '_') + '.png'
    image_path = os.path.join(image_dir, image_name)
    response = requests.get(url)
    cookies = response.cookies.get_dict()
    print(url)
    cat_img = response.content
    with open(image_path, 'wb') as f:
        f.write(cat_img)
        f.close()
    return image_path, cert, cookies


def input_verify_code(code, cert, cookies):
    post_url = 'http://mp.weixin.qq.com/mp/verifycode'
    data = {
        'cert': cert,
        'input': code,
        'appmsg_token': ''
    }
    res = requests.post(url=post_url, data=data, cookies=cookies)
    if res.status_code == 200:
        return res.text


def input_code_by_url(url):
    res = requests.get(url)
    # 生成一个随机数cert
    cookies = res.cookies.get_dict()
    print(cookies)
    cert = int(time.time()*1000) + round(random.random(), 3)
    print('生成随机数: {}'.format(cert))
    image_url = 'http://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
    image_path, cert, tmp_cookies = save_verify_image(image_url)
    print(tmp_cookies)
    cookies['sig'] = tmp_cookies.get('sig')
    print(cookies)
    code = get_verify_code(image_path)
    print('返回验证码:{}'.format(code))
    input_verify_code(code, cert, cookies)

