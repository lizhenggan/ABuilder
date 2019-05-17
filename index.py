# encoding: utf-8
"""
@author: 李果 Aiden
@contact: 1334435738@qq.com
@file: index.py
@time: 2019-05-15 14:36
@desc:
"""
from ABuilder.ABuilder import ABuilder

model = ABuilder()
data = model.table('tar_user').field("username,id").where({"username": ["like", "%M-萌%"]}).limit(0, 1).query()
print(data)
