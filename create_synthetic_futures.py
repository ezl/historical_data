import numpy as np
from bananas.db.sqliteutils import open_db, create_table_if_not_exists, insert_record
from bananas.dataframe.dataframe import dataframe, execute_query_DF
import datetime
import pdb

dbname = "data/filteredcornDB.sqlite3"
start_date = datetime.date(2010, 1, 14)

conn = open_db(dbname)

SQL_trade_dates = """SELECT DISTINCT trade_date FROM Futures WHERE trade_date > '%s'""" % start_date
df = execute_query_DF(conn, SQL_trade_dates)

trade_dates = df('trade_date')

SQL_get_futures_for_trade_date = """SELECT * FROM FUTURES where trade_date='%s'"""
SQL_get_futures_all = """SELECT * FROM FUTURES"""

def get_synthetic_maturity_future(days, trade_date, expiration_dates, prices):
    """Create a synthetic 'n-day out' maturity future.

       Requires the futures curve with prices, expiration dates, and the 
       calculation date (trade_date).

       Inputs:
           days               <integer> The maturity of the synthetic future
                              you want. For a synthetic 90 day future, days=90.
           trade_date:        <datetime> The calculation date from which the
                              n-day maturity is computed AND used to determine
                              how far out each future is based on the
                              expiration_dates input.


#TODO NOT LISTS! only numpy arrays.  also trade_date can be a datetime or a np array of datestimes where trade_date.shape=expiration_dates.shape

           expiration_dates:  <list> or <numpy array> Expiration date for each
                              forward price.  Must be the same size as "prices".
                              expiration_dates - trade_date is used to determine
                              how many days to expiration each forward price is
                              and then interpolate the synthetic forward.
           prices:            <list> or <numpy array> Forward prices that
                              correspond to expiration_dates.  Values should be
                              floats. Must be same size as expiration_dates.
       Returns:
           synth_fut:         <float> the n-day maturity synthetic forward price.
    """
    if any(prices==0):
        return -999999999
    return linear_interpolation_for_synthetic_maturity_future(days, trade_date, expiration_dates, prices)

def linear_interpolation_for_synthetic_maturity_future(days, trade_date, expiration_dates, prices):
    """Linearly interpolate.

       Will break if it can't find a future on each side of the requested maturity.

       Moving the garbage to another function so the real function can be properly implemented at a later date.

       TODO: For now, this will just linearly interpolate between the nearest 2
             surrounding futures. Should rewrite.  This will serve initial purpose
             though for only a 90 day interpolated price for hist vol studies.
    """
    dte = [i.days for i in (expiration_dates - trade_date)]
    try:
        synth_fut = np.interp(days, dte, prices)
    except:
        pdb.set_trace()
    return synth_fut


if __name__ == "__main__":
    records = []
    for trade_date in trade_dates:
        df = execute_query_DF(conn, SQL_get_futures_for_trade_date % trade_date)
        closes = df("px_close")
        settles = df("px_settle")
        prices = settles
        expiration_dates = df("exp_date")
        synth = get_synthetic_maturity_future(days=90, trade_date=trade_date, expiration_dates=expiration_dates, prices=prices)
        records.append((trade_date, synth))
