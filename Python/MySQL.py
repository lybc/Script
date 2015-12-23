# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'lybc'

import MySQLdb
import time

class MySQL:

    _instance = None # 本类的实例
    _conn = None     # 数据库conn
    _cur = None      # 游标

    _TIMEOUT = 30 #默认超时30秒
    _timecount = 0
    log_file = None

    def __init__(self, dbconfig):
        self.log_file = open('SQLException.log', 'w')
        try:
            self._conn = MySQLdb.connect(
                host=dbconfig['host'],
                port=dbconfig['port'],
                user=dbconfig['user'],
                passwd=dbconfig['passwd'],
                db=dbconfig['db'],
                charset=dbconfig['charset']
            )
        except MySQLdb.Error, e:
            error_msg = 'MySQL ERROR %d: %s' % (e.args[0], e.args[1])
            print(error_msg)
            self.log_file.write(error_msg)
        self._cur = self._conn.cursor(MySQLdb.cursors.DictCursor)


    def find_all(self, table_name, condition='', params=list):
        sql = "SELECT * FROM "
        if table_name:
            sql += table_name
        if condition:
            sql += ' WHERE ' + condition
        try:
            if params:
                self._cur.execute(sql, params)
            else:
                self._cur.execute(sql)
            return self._cur.fetchall()
        except MySQLdb.Error, e:
            error_msg = 'MySQL ERROR %d: %s' % (e.args[0], e.args[1])
            print(error_msg)
            self.log_file.write(error_msg)

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'lenovo',
    'charset': 'utf8'
}
db = MySQL(config)
print(time.time())
print db.find_all('Vendor',params=[])
print(time.time())