#-*- encoding: utf-8 -*-

import psycopg2
from psycopg2.extras import RealDictCursor


class PGSQLUtil:
    """
    PostgreSQL工具类
    """
    def __init__(self, host="127.0.0.1", user=None, password=None, database=None, port=5432, dsn=None, connection_factory=None, cursor_factory=None, **kwargs):
        """构造函数"""
        self.__database = database
        self.__conn = psycopg2.connect(host=host, user=user, password=password, database=database, port=str(port),
                                       dsn=dsn, connection_factory=connection_factory, cursor_factory=cursor_factory, **kwargs)
        """只显示数据不显示字段名"""
        self.__cursor = self.__conn.cursor()

    def __del__(self):
        """析构函数"""
        self.__cursor.close()
        self.__conn.close()

    def get_conn(self):
        """获取连接"""
        return self.__conn

    def get_cursor(self):
        """获取游标"""
        return self.__cursor

    def list_databases(self, vars=None):
        """查询所有数据库"""
        self.__cursor.execute("SELECT pg_database.datname FROM pg_database", vars)
        dbs = []
        for db in self.__cursor.fetchall():
            dbs.append(db[0])
        return dbs

    def list_user_tables(self, vars=None):
        """查询当前用户所有表"""
        self.__cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'", vars)
        # self.__cursor.execute("SELECT * FROM  information_schema.tables WHERE table_schema='public'", vars)
        tables = []
        for table in self.__cursor.fetchall():
            tables.append(table[0])
        return tables

    def list_tables_privileges(self, vars=None):
        """查询所有表的权限"""
        self.__cursor.execute("SELECT * FROM  information_schema.table_privileges", vars)
        return self.__cursor.fetchall()

    def execute_c(self, sql, vars=None):
        """获取SQL执行结果"""
        # self.__cursor = self.__conn.cursor(cursor_factory=RealDictCursor)
        self.__cursor.execute(sql, vars)
        return self.__cursor.fetchall()

    def execute_aud(self, sql, vars=None):
        """获取SQL执行结果"""
        # self.__cursor = self.__conn.cursor(cursor_factory=RealDictCursor)
        self.__cursor.execute(sql, vars)
        self.get_conn().commit()

    def get_version(self, vars=None):
        """获取MySQL版本"""
        self.__cursor.execute("SELECT VERSION()", vars)
        version = self.__cursor.fetchone()
        print("Postgresql Version : %s" % version)
        return version[0]

    def list_table_metadata(self, vars=None):
        """查询所有表的元数据信息"""
        sql = "SELECT * FROM information_schema.TABLES WHERE TABLE_TYPE !='SYSTEM VIEW' AND TABLE_SCHEMA NOT IN ('sys','mysql','information_schema','performance_schema')"
        self.__cursor.execute(sql, vars)
        return self.__cursor.fetchall()

    def get_table_fields(self, table, vars=None):
        """获取表字段信息"""
        sql = "SELECT column_name FROM information_schema.COLUMNS WHERE table_schema='public' AND table_name='"+ table +"'"
        self.__cursor.execute(sql, vars)
        fields = []
        for field in self.__cursor.fetchall():
            fields.append(field[0])
        return fields

    def table_metadata(self, table, vars=None):
        """获取表字段信息"""
        sql = "SELECT * FROM information_schema.COLUMNS WHERE table_schema='public' AND table_name='"+ table +"'"
        self.__cursor.execute(sql, vars)
        fields = []
        for field in self.__cursor.fetchall():
            fields.append(field)
        return fields


if __name__ == "__main__":
    pgsqlUtil = PGSQLUtil(host="127.0.0.1", user="yaokz", password="yaokz1314", database="myroot")
    pgsqlUtil.get_version()
    conn = pgsqlUtil.get_conn()
    ## 查询所有数据库
    databases = pgsqlUtil.list_databases()
    print(type(databases), databases)
    ## 查询当前用户的表
    tables = pgsqlUtil.list_user_tables()
    print(type(tables), tables)
    ## 查询所有表的权限信息
    privileges = pgsqlUtil.list_tables_privileges()
    for privilege in privileges:
        print(privilege)
    ## 查询表数据
    result = pgsqlUtil.execute("SELECT * FROM pg_user")
    for i in result:
        print(i)

    # result = pgsqlUtil.get_table_fields("pg_user")
    result = pgsqlUtil.table_metadata("pg_user")
    for i in result:
        print(i)