from tools.sqliteutils import open_db, create_table_if_not_exists, insert_record
from tools.dataframe import dataframe, execute_query_DF

dbname = "data/filteredcornDB.sqlite3"

conn = open_db(dbname)

SQL_trade_dates = """SELECT DISTINCT trade_date FROM Futures"""
df = execute_query_DF(conn, SQL_trade_dates)

trade_dates = df('trade_date')

trade_date = trade_dates[0]

SQL_get_futures_for_trade_date = """SELECT * FROM FUTURES where trade_date='%s'""" % trade_date
SQL_get_futures_all = """SELECT * FROM FUTURES"""

df = execute_query_DF(conn, SQL_get_futures_all)


