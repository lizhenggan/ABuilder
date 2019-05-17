# encoding: utf-8
"""
@author: 李果
@contact: 1334435738@qq.com
@file: db.py
@time: 2019/3/7 5:32 PM
@desc:
"""
from database import database
import pymysql
import logging

db_config = {'host': database.data_host, 'port': database.data_port, 'user': database.data_user,
             'password': database.data_pass,
             'db': database.database, 'charset': database.charset, 'cursorclass': pymysql.cursors.DictCursor}


class Db(object):
    def __init__(self, conn=None, slave=False, bid=''):
        if conn:
            self.conn = conn
        else:
            self.conn = pymysql.connect(**db_config)
        self.cur = self.conn.cursor()
        self.res = True

    def __del__(self):
        self.finish()

    def execute(self, sql, param=None):
        try:
            if 'select' not in sql.lower()[:7]:
                logging.info(sql)
            else:
                logging.info(sql)
                logging.debug(sql)
            if not param:
                return self.cur.execute(sql)
            else:
                return self.cur.execute(sql, param)
        except:
            self.res = False
            logging.error(u"DB error: %s" % sql, exc_info=True)
            return 0
        finally:
            pass
            # self.ObjClass.init_data()

    def get_first(self, sql, param=None):
        self.execute(sql, param)
        return self.cur.fetchone()

    def select(self, sql, param=None):
        self.execute(sql, param)
        return self.cur.fetchall()

    def do_insert(self, sql, last=False):
        state = self.execute(sql)
        return self.cur.lastrowid if (last is True) else state

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def finish(self):
        if self.res:
            self.conn.commit()
        else:
            self.conn.rollback()
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
