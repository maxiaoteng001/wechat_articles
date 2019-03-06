# -*- coding: utf-8 -*-

# __        __        _           _   ____
# \ \      / /__  ___| |__   __ _| |_/ ___|  ___   __ _  ___  _   _
#  \ \ /\ / / _ \/ __| '_ \ / _` | __\___ \ / _ \ / _` |/ _ \| | | |
#   \ V  V /  __/ (__| | | | (_| | |_ ___) | (_) | (_| | (_) | |_| |
#    \_/\_/ \___|\___|_| |_|\__,_|\__|____/ \___/ \__, |\___/ \__,_|
#                                                 |___/

"""
WechatSogou Crawler Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from wechatsogou_yf.api import WechatSogouAPI
from wechatsogou_yf.const import WechatSogouConst
from wechatsogou_yf.request import WechatSogouRequest
from wechatsogou_yf.structuring import WechatSogouStructuring
from wechatsogou_yf.exceptions import WechatSogouException, WechatSogouVcodeOcrException, WechatSogouRequestsException

__all__ = [
    'WechatSogouConst',

    'WechatSogouAPI',
    'WechatSogouRequest',
    'WechatSogouStructuring',

    'WechatSogouException',
    'WechatSogouVcodeOcrException',
    'WechatSogouRequestsException']

__title__ = 'wechatsogou_yf'
__version__ = "4.2.1"
__author__ = 'Chyroc'

"""doc string

https://www.jetbrains.com/help/pycharm/type-hinting-in-pycharm.html
https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
"""
