# encoding: utf-8
"""
@author: 李果 Aiden
@contact: 1334435738@qq.com
@file: validate.py
@time: 2019/3/29 3:30 PM
@desc:
"""


class Validate:
    def where_format(self, where):
        state, error = self.typeof_dict(where)
        if state is True:
            for item in where:
                if isinstance(where[item], list) is False:
                    error = 'Where format error, example:{"id":["=",888]}'
                    break
                elif len(where[item]) is not 2:
                    error = 'Where is a list of length 2, example:["=",2]'
                    break

        if error is not None:
            raise Exception(error)

        return True

    def insert_format(self, data, types="Insert data"):
        state, error = self.typeof_dict(data, types)
        if error is not None:
            raise Exception(error)
        return True

    @staticmethod
    def typeof_dict(param, types='Where'):
        error = None
        if isinstance(param, dict) is False:
            error = '%s is not Dict' % types
        elif param == {}:
            error = "%s can't be empty" % types

        return (True, error) if error is None else (False, error)
