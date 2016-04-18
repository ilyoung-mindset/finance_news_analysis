# encoding=utf-8

import sys
import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

from mysql_config import DATABASE_CONFIG
from mysql_connection import MySQLConnection
from mysql_init import init_mysql


class MySQLPool(object):
    ''' Python Class for connecting with MySQL server \
    and accelerate development project using MySQL'''

    __instance = None

    @staticmethod
    def getSingleConnection():
        conn = MySQLdb.connect(
            DATABASE_CONFIG['HOST'],
            DATABASE_CONFIG['USER'],
            DATABASE_CONFIG['PASSWORD'],
            DATABASE_CONFIG['DATABASE'],
            charset='utf8',
            use_unicode=True,
            cursorclass=DictCursor
        )
        wraped_conn = MySQLConnection(conn)
        return wraped_conn

    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(MySQLPool, cls).__new__(
                cls, *args, **kwargs)
        return cls.__instance
    # End def __new__

    def __init__(self, min_conn=2):
        init_mysql()
        self.__host = DATABASE_CONFIG['HOST']
        self.__user = DATABASE_CONFIG['USER']
        self.__password = DATABASE_CONFIG['PASSWORD']
        self.__database = DATABASE_CONFIG['DATABASE']
        self.__min_conn = min_conn
        self.__pool = PooledDB(
            MySQLdb,
            self.__min_conn,
            host=self.__host,
            user=self.__user,
            passwd=self.__password,
            db=self.__database,
            charset='utf8',
            use_unicode=True,
            cursorclass=DictCursor)
    # End def __init__

    def getConnection(self):
        try:
            conn = self.__pool.connection()
            wraped_conn = MySQLConnection(conn)
            return wraped_conn
        except MySQLdb.Error as e:
            sys.stderr.write("Error %d: %s\n" % (e.args[0], e.args[1]))
            return None
    # End def __open
# End class


def main():
    mysql = MySQLPool()
    conn = mysql.getConnection()
    return conn
    pass


if __name__ == '__main__':
    main()