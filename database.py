# encoding: utf-8
"""
@author: 李果 Aiden
@contact: 1334435738@qq.com
@file: database.py
@time: 2019-05-15 14:53
@desc:
"""


class Pro(object):
    pass


class Dev(object):
    debug = True
    DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/name'
    data_host = '127.0.0.1'
    data_pass = '***'
    data_user = 'root'
    database = 'name'
    data_port = 3306
    charset = 'utf8mb4'


database = Dev
