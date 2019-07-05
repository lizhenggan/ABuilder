# encoding: utf-8
"""
@author: 李果 Aiden
@contact: 1334435738@qq.com
@file: build.py
@time: 2019/3/27 5:52 PM
@desc:
"""
from .validate import *


class Builder:
    _table_name = ''
    _where_str = ''
    _where_or_str = ''
    _field_str = '*'
    _order_str = ''
    _group_str = ''
    _limit_str = ''
    _param_list = []
    _execute_sql = ''
    _join_list = []

    def _assemble(self):
        """
        组装sql
        :return:
        """
        sql = "select {} from {}".format(self._field_str, self._table_name)

        if self._join_list:
            for item in self._join_list:
                sql = "%s %s" % (sql, item)
        if self._where_str:
            sql = "%s where %s" % (sql, self._where_str)
        if self._where_or_str:
            sql = "%s or (%s)" % (sql, self._where_or_str) if self._where_str \
                else "%s where %s" % (sql, self._where_or_str)
        if self._group_str:
            sql = "%s group by %s" % (sql, self._group_str)
        if self._order_str:
            sql = "%s order by %s" % (sql, self._order_str)
        if self._limit_str:
            sql = "%s%s" % (sql, self._limit_str)

        self.__last_sql = sql % tuple(self._param_list)
        return sql

    def table(self, name):
        """
        set table
        :param name:
        :return:
        """
        self._init_data()
        self._table_name = name
        return self

    def where(self, where, splicing='and'):
        """
        where
        :param where:
        :param splicing:
        :return:
        """
        Validate().where_format(where)
        string = ''
        for item in where:
            string = "%s%s" % (string, "%s%s %s %s" % ('' if string == '' else " and ", item, where[item][0], '%s'))
            self._param_list.append(where[item][1])

        self._where_str = string if self._where_str == '' else "%s %s %s" % (self._where_str, splicing, string)
        return self

    def where_or(self, where, splicing='or'):
        """
        where or
        :param where:
        :param splicing:
        :return:
        """
        Validate().where_format(where)
        string = ''
        for item in where:
            string = "%s%s" % (string, "%s%s %s %s" % ('' if string == '' else " or ", item, where[item][0], '%s'))
            self._param_list.append(where[item][1])
        self._where_or_str = string if self._where_or_str == '' else "%s %s %s" % (self._where_or_str, splicing, string)
        return self

    def field(self, string='*'):
        """
        set field
        :param string:
        :return:
        """
        self._field_str = string
        return self

    def order(self, string, sort='asc'):
        """
        order by
        :param string:
        :param sort:
        :return:
        """
        self._order_str = ("%s %s" if self._order_str == '' else "{},%s %s".format(self._order_str)) % (string, sort)
        return self

    def group(self, string):
        """
        group
        :param string:
        :return:
        """
        self._group_str = string if self._group_str == '' else "%s,%s" % (self._group_str, string)
        return self

    def limit(self, start, end):
        """
        limit
        :param start:
        :param end:
        :return:
        """
        self._limit_str = " limit %d,%d" % (start, end)
        return self

    def join(self, table, where, prefix="INNER"):
        self._join_list.append("%s JOIN %s on %s" % (prefix, table, where))
        return self

    def update_sql(self, param):
        """
        update
        :param param:
        :return:
        """
        Validate().insert_format(param, types='Update data')
        set_str = ''
        params = []
        for item in param:
            string = "{}=%s".format(item)
            set_str = "%s%s" % (set_str, "%s" % string if set_str == '' else ',%s' % string)
            params.append(param[item])
        self._param_list = params + self._param_list
        self._execute_sql = "update %s SET %s where %s" % (self._table_name, set_str, self._where_str)

    def delete_sql(self):
        self._execute_sql = "delete from %s where %s" % (self._table_name, self._where_str)

    def insert_sql(self, param):
        """
        insert
        :param param:
        :return:
        """

        Validate().insert_format(param)
        field = value = None
        for item in param:
            if field is None:
                field = item
                value = "%s"
            else:
                field = ("%s,%s" % (field, item))
                value = ("{},{}".format(value, "%s"))

            self._param_list.append(param[item])
        self._execute_sql = "insert into %s (%s) values (%s)" % (self._table_name, field, value)

    def _init_data(self):
        """
        初始化
        :return:
        """
        self._table_name = ''
        self._where_str = ''
        self._where_or_str = ''
        self._field_str = '*'
        self._order_str = ''
        self._group_str = ''
        self._limit_str = ''
        self._param_list = []
        self._execute_sql = ''
        self._join_list = []
