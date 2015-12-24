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
            error_msg = '   MySQL ERROR %d: %s' % (e.args[0], e.args[1])
            print(error_msg)
            self.log_file.write(time.strftime('%Y-%m-%d %X',time.localtime()) + error_msg)
        self._cur = self._conn.cursor(MySQLdb.cursors.DictCursor)


    def find_all(self, sql):
        try:
            self._cur.execute(sql)
            return self._cur.fetchall()
        except MySQLdb.Error, e:
            error_msg = '   MySQL ERROR %d: %s' % (e.args[0], e.args[1])
            print(error_msg)
            self.log_file.write(time.strftime('%Y-%m-%d %X',time.localtime()) + error_msg)

    def exec_sql(self, sql):
        try:
            return self._cur.execute(sql)
        except MySQLdb.Error, e:
            error_msg = '   MySQL ERROR %d: %s' % (e.args[0], e.args[1])
            print(error_msg)
            self.log_file.write(time.strftime('%Y-%m-%d %X',time.localtime()) + error_msg)

    def transaction(self, sql_list):
        if isinstance(sql_list, []):
            try:
                for sql in sql_list:
                    self._cur.execute(sql)
                self._conn.commit()
            except MySQLdb.Error, e:
                self._conn.rollback()
                error_msg = '   MySQL ERROR %d: %s' % (e.args[0], e.args[1])
                print(error_msg)
                self.log_file.write(time.strftime('%Y-%m-%d %X',time.localtime()) + error_msg)


    def __del__(self):
        self._cur.close()
        self._conn.close()

    def close(self):
        self.__del__()


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
sql = 'select * from Vendor where'
print db.find_all(sql)
print(time.time())