import numpy as np
from bananas.db.sqliteutils import open_db, create_table_if_not_exists, insert_record
from bananas.dataframe.dataframe import dataframe, execute_query_DF
import datetime
import pdb
from matplotlib import pyplot

dbname = "data/filteredcornDB.sqlite3"
start_date = datetime.date(2009, 1, 1)

conn = open_db(dbname)

SQL_trade_dates = """SELECT DISTINCT trade_date FROM Futures WHERE trade_date > '%s'""" % start_date
df = execute_query_DF(conn, SQL_trade_dates)

trade_dates = df('trade_date')

SQL_get_futures_for_trade_date = """SELECT * FROM FUTURES where trade_date='%s'"""
SQL_get_futures_all = """SELECT * FROM FUTURES"""

prices_list = []
expiration_dates_list = []
trade_date_list = []

for trade_date in trade_dates:
    df = execute_query_DF(conn, SQL_get_futures_for_trade_date % trade_date)
    closes = df("px_close")
    settles = df("px_settle")
    prices = closes
    expiration_dates = df("exp_date")

    expiration_dates_list.append(expiration_dates)
    prices_list.append(prices)
    trade_date_list.append(trade_date)
    print trade_date

from bananas.anim import animate

animate(x_list=expiration_dates_list, y_list=prices_list, title_list=trade_date_list, interval=0)
