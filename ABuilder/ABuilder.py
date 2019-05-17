# encoding: utf-8
"""
@author: 李果
@contact: 1334435738@qq.com
@file: db.py
@time: 2019/3/7 5:32 PM
@desc:
"""
from .Library.builder import Builder
from .Library.db import Db


class ABuilder(Builder, Db):
    __last_sql = ''
    __insert_id = 0

    @property
    def get_last_sql(self):
        return self.__last_sql

    @property
    def get_insert_id(self):
        return self.__insert_id

    def query(self):
        """
        查询多条
        :return:
        """
        sql = self._assemble()
        return self.select(sql, self._param_list)

    def first(self):
        """
        查询单条
        :return:
        """
        sql = self._assemble()
        return self.get_first(sql, self._param_list)

    def update(self, param):
        """
        update
        :param param:
        :return:
        """
        self.update_sql(param)
        self.__last_sql = self._execute_sql % tuple(self._param_list)
        state = self.execute(self._execute_sql, self._param_list)
        return state

    def insert(self, param):
        """
        insert
        :param param:
        :return:
        """
        self.insert_sql(param)
        state = self.execute(self._execute_sql, self._param_list)
        self.__insert_id = self.cur.lastrowid
        self.__last_sql = self._execute_sql
        return state

    def delete(self):
        """
        删除
        :return:
        """
        self.delete_sql()
        state = self.execute(self._execute_sql, self._param_list)
        self.__last_sql = self._execute_sql % tuple(self._param_list)
        return state

    def pluck(self, field):
        """
        查询单个字段
        :param field:
        :return:
        """
        self.field(field)
        result = self.first()
        return result[field] if result else ''
