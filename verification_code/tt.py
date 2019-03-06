import ydm_verify_code
import requests
from bs4 import BeautifulSoup
import time
import random

url = 'http://mp.weixin.qq.com/profile?src=3&timestamp=1543830857&ver=1&signature=Hr7uxm3RhF6Hj5CyJ7h0prIaJRFXSfdhuLJe6SqntpThBhiLM2NrBPK5Y7CWKW-DzYETAUpx1X1utXnktKVAmA=='


# res = requests.get(url)
# html_soup = BeautifulSoup(res.text, "html.parser")
# print(res.text)
# verify_img_tag = html_soup.find('img', {'id': 'verify_img'})
# verify_img_url = 'http://mp.weixin.qq.com' + verify_img_tag.get('src')
# print(verify_img_url)

# ydm_verify_code.input_code_by_url(verify_img_url)

result = int(time.time()*1000) + round(random.random(), 3)
print(result)


import hashlib
hl = hashlib.md5()
hl.update(url.encode(encoding='utf-8'))
new = hl.hexdigest()
print(new)

import os
s = os.path.join(os.path.dirname(os.path.realpath(__file__)), '')
print(s)