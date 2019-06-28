"""
author wanghaiying
date 20190601
description python操作mysql的工具类
"""
import pymysql
import _thread
import time

sql_lock = _thread.allocate_lock()
from schedule.config import *


class MysqlUtil:
    def __init__(self):
        # sys.path.append("../")
        self._host = mysql_host
        self._port = mysql_port
        self._user = mysql_user
        self._passwd = mysql_passwd
        self._db = mysql_db
        if not self._connectMysql(): assert "Can't connect to the MySQL server."
        self.checkConn()

    def _connectMysql(self):
        try:
            self._conn = pymysql.connect(self._host, self._user, self._passwd, self._db)
            self._cursor = self._conn.cursor()
            return True
        except:
            return False

    def checkConn(self):
        life = 5
        while True:
            try:
                self._conn.ping()
                return True
            except Exception as e:
                print(e)
                life -= 1
                if self._connectMysql():
                    return True
                time.sleep(1)
                if life > 0:
                    continue
                print("Can't connect to the MySQL server.")
                return False

    def insert(self, sql, id=False):
        sql_lock.acquire()
        res = True
        try:
            self.checkConn()
            self._cursor.execute(sql)
            if id: res = self._cursor.lastrowid
        except pymysql.Error as e:
            print("Error: %s" % e)
            res = False
        finally:
            self._conn.commit()
            sql_lock.release()
            return res

    def select(self, sql):
        sql_lock.acquire()
        res = False
        try:
            self.checkConn()
            self._cursor.execute(sql)
            res = self._cursor.fetchall()
        except Exception as e:
            print("Error: %s" % e)
        finally:
            sql_lock.release()
            return res

    def update(self, sql):
        sql_lock.acquire()
        res = True
        try:
            self.checkConn()
            res = self._cursor.execute(sql)
            print(res)
        except pymysql.Error as e:
            print("Error: %s" % e)
            res = False
        finally:
            self._conn.commit()
            sql_lock.release()
            return res


if __name__ == '__main__':
    mysqlUtil = MysqlUtil()
    # result = mysqlUtil.select("select * from tasktype")
    result = mysqlUtil.update("update tasktype set description = '这是ST任务' where tasktype='ST'")
    print(result)
