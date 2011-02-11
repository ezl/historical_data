import numpy as np
from bananas.db.sqliteutils import open_db, create_table_if_not_exists, insert_record
from bananas.dataframe.dataframe import dataframe, execute_query_DF
from bananas.ipshell import ipshell
import datetime
import time
import pdb
from matplotlib import pyplot
from create_synthetic_futures import get_synthetic_maturity_future


"""Animate slides of every term structure.  Blue dot is the prices, Red dot is a synthetic maturity"""

freeze_dates = [datetime.date(1996,4,4),
                datetime.date(1996,4,5), # limit day
                datetime.date(1996,4,9),

                datetime.date(1994,3,31),
                datetime.date(1994,4,1), # probably limit down
                datetime.date(1994,4,4),

                datetime.date(1992,4,10),
                datetime.date(1992,4,13), # NO IDEA WHY THIS DAY HAS NO DATA. EXPLAIN!
                datetime.date(1992,4,15),

                datetime.date(1993,12,30),
                datetime.date(1993,12,31), # new years eve
                datetime.date(1994,1,03),

                datetime.date(1999,12,29),
                datetime.date(1999,12,30),
                datetime.date(1999,12,31), # a friday, but no price data. probable holiday, but why is there an entry at all?
                datetime.date(2000,1,3),   # also, oddly there is a NOV future in this set

                datetime.date(2001,9,10),
                datetime.date(2001,9,11), # 9/11
                datetime.date(2001,9,12), # 9/11
                datetime.date(2001,9,13),

                datetime.date(2001,12,21),
                datetime.date(2001,12,24), # xmas eve, monday.  meaning that 4 days were off in a row in 2001
                datetime.date(2001,12,26),

                datetime.date(2002,12,23),
                datetime.date(2002,12,24), # xmas eve
                datetime.date(2002,12,26),

                datetime.date(1978,11,6),
                datetime.date(1978,11,8), # no settlement prices, but seemingly good closing prices. use close this day?
                datetime.date(1978,11,9),

                datetime.date(1977,4,29),
                datetime.date(1977,5,2), # 16 cent move from 4/29 to 5/2, but no price data on 5/2.  uncertain if limit?
                datetime.date(1977,5,3),

                datetime.date(2010,9,14),
                datetime.date(2010,9,15),
                datetime.date(2010,9,16),
               ]

dbname = "data/filteredcornDB.sqlite3"
start_date = datetime.date(1980, 1, 1)
end_date = datetime.date(2011, 1, 10)

""" Shitty period with doubled up contracts of weird prices"""
# start_date = datetime.date(1996, 6, 1)
# end_date = datetime.date(1997, 6, 10)

""" TEST"""
# start_date = datetime.date(1992, 4, 1)
# end_date = datetime.date(1992, 6, 10)

conn = open_db(dbname)

SQL_trade_dates = """SELECT DISTINCT trade_date FROM Futures WHERE trade_date > '%s' AND trade_date < '%s'""" % (start_date, end_date)
df = execute_query_DF(conn, SQL_trade_dates)

trade_dates = df('trade_date')

SQL_get_futures_for_trade_date = """SELECT * FROM FUTURES where trade_date='%s'"""
SQL_get_futures_all = """SELECT * FROM FUTURES"""

prices_list = []
expiration_dates_list = []
trade_date_list = []


# to calculate historical realized vol
synth_fut_list = []

pyplot.ion()
ax = pyplot.subplot(111)
line, = pyplot.plot(0, 0, "bo")
dot, = pyplot.plot(0, 0, "ro")

interval = 0
ylim_window = 12
synth_maturity = 100
DEBUG = False

for trade_date in trade_dates:
    if DEBUG:
        if trade_date in freeze_dates:
            print expiration_dates
            print settles
            print closes
            ipshell()

    df = execute_query_DF(conn, SQL_get_futures_for_trade_date % trade_date)
    closes = df("px_close")
    settles = df("px_settle")
    prices = settles
    expiration_dates = df("exp_date")

    if trade_date == datetime.date(1997, 1, 20):
        pass
        # weird day.
        # ipshell()


    bad_prints = (prices > 8000) + (prices < 10)
    if any(bad_prints):
        print "-" * 20
        print expiration_dates
        print prices
        prices = prices[-bad_prints]
        expiration_dates = expiration_dates[-bad_prints]

    if all(bad_prints):
        trade_dates = trade_dates[trade_dates != trade_date]
        continue
    # this is a hacky way to thow away some of the bad data.  just assuming zero vol on zero price days or stupid price days. (copy last days price)
    synth_fut = get_synthetic_maturity_future(days=synth_maturity, trade_date=trade_date, expiration_dates=expiration_dates, prices=prices)
    if synth_fut < 10 or synth_fut > 10000:
        synth_fut_list.append(synth_fut_list[-1]) # or NANNNANANANANNNANANNANNANNANNNANNNANNNAN
    else:
        synth_fut_list.append(synth_fut)

    expiration_dates_list.append(expiration_dates)
    prices_list.append(prices)
    trade_date_list.append(trade_date)
    print trade_date

    ax.set_title(trade_date)
    line.set_xdata(expiration_dates)
    line.set_ydata(prices)
    dot.set_xdata([trade_date + datetime.timedelta(days=synth_maturity), ])
    dot.set_ydata([synth_fut, ])

    xmin = trade_date - datetime.timedelta(days=30)
    xmax = np.max(expiration_dates) + datetime.timedelta(days=30)
    ymin = np.mean( [np.min(i) for i in prices_list[-ylim_window:]] ) - 500
    ymax = np.mean( [np.max(i) for i in prices_list[-ylim_window:]] ) + 500
    #pdb.set_trace()

    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    pyplot.draw()
    time.sleep(interval)

# calculate historical realized vo
vol_window = 22 # trading days
days_per_year = 270.08
trade_dates,
logdiffs = np.hstack((np.nan, np.diff(np.log(np.array(synth_fut_list))) ** 2))
historical_vol = np.hstack((np.nan * np.ones(vol_window -1)     ,   np.sqrt(np.convolve(logdiffs, np.ones(vol_window), mode="valid") * days_per_year / vol_window ) ))

pyplot.plot(trade_dates, historical_vol, "r-")
pyplot.figure()
pyplot.plot(trade_dates, synth_fut_list)

# from anim import animate
# animate(x_list=expiration_dates_list, y_list=prices_list, title_list=trade_date_list, interval=0.25)
