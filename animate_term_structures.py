import numpy as np
from bananas.db.sqliteutils import open_db, create_table_if_not_exists, insert_record
from bananas.dataframe.dataframe import dataframe, execute_query_DF
import datetime
import time
import pdb
from matplotlib import pyplot
from create_synthetic_futures import get_synthetic_maturity_future


"""Animate slides of every term structure.  Blue dot is the prices, Red dot is a synthetic maturity"""

dbname = "data/filteredcornDB.sqlite3"
start_date = datetime.date(1977, 1, 1)

conn = open_db(dbname)

SQL_trade_dates = """SELECT DISTINCT trade_date FROM Futures WHERE trade_date > '%s'""" % start_date
df = execute_query_DF(conn, SQL_trade_dates)

trade_dates = df('trade_date')

SQL_get_futures_for_trade_date = """SELECT * FROM FUTURES where trade_date='%s'"""
SQL_get_futures_all = """SELECT * FROM FUTURES"""

prices_list = []
expiration_dates_list = []
trade_date_list = []


pyplot.ion()
ax = pyplot.subplot(111)
line, = pyplot.plot(0, 0, "bo")
dot, = pyplot.plot(0, 0, "ro")

interval = 0
ylim_window = 12
synth_maturity = 90
for trade_date in trade_dates:
    df = execute_query_DF(conn, SQL_get_futures_for_trade_date % trade_date)
    closes = df("px_close")
    settles = df("px_settle")
    prices = settles
    expiration_dates = df("exp_date")
    synth_fut = get_synthetic_maturity_future(days=synth_maturity, trade_date=trade_date, expiration_dates=expiration_dates, prices=prices)

    expiration_dates_list.append(expiration_dates)
    prices_list.append(prices)
    trade_date_list.append(trade_date)
    print trade_date

    DEBUG = False
    if DEBUG:
        freeze_dates = [datetime.date(2010,3,15), datetime.date(2010,3,16), datetime.date(2010,4,2)]
        if trade_date in freeze_dates:
            pdb.set_trace()

    ax.set_title(trade_date)
    line.set_xdata(expiration_dates)
    line.set_ydata(prices)
    dot.set_xdata([trade_date + datetime.timedelta(days=synth_maturity), ])
    dot.set_ydata([synth_fut, ])

    xmin = trade_date
    xmax = np.max(expiration_dates) + datetime.timedelta(days=30)
    ymin = np.mean( [np.min(i) for i in prices_list[-ylim_window:]] ) - 1000
    ymax = np.mean( [np.max(i) for i in prices_list[-ylim_window:]] ) + 1000
    #pdb.set_trace()

    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    pyplot.draw()
    time.sleep(interval)


# from anim import animate

# animate(x_list=expiration_dates_list, y_list=prices_list, title_list=trade_date_list, interval=0.25)
