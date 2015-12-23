# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'lybc'

import MySQLdb
import time

class MySQL:
    error_code = ''

    _instance = None # 本类的实例
    _conn = None     # 数据库conn
    _cur = None      # 游标

    _TIMEOUT = 30 #默认超时30秒
    _timecount = 0

    def __init__(self, dbconfig):
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
            self.error_code = e.args[0]
            error_msg = 'MySQL ERROR: ', e.args[0], e.args[1]

            if self._timecount < self._TIMEOUT:
                interval = 5
                self._timecount += interval
                time.sleep(interval)
                return self.__init__(dbconfig)
            else:
                raise Exception(error_msg)
        self._cur = self._conn.cursor()
        self._instance = MySQLdb