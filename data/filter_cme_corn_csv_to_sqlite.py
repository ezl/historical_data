"""Take a row from the CME EOD data and removes fields I don't care about to create a curated sqlite DB.

   Most of these fields are designed to coincide with the data format I'm capturing going forward from the cme settlements on the website.

   File dumps data into a new SQLite file with 2 tables: Futures (product_symbol==C), Options (product_symbol==PY). 8CC and CCZ are discarded.
"""

from bananas.db.sqliteutils import open_db, create_table_if_not_exists, insert_record
import sys
import datetime

def datamine_date_to_datetime(datamine_date):
    """Convert CME Datamine date to python datetime.

       CME Datamine dates are "mmddyy".
       Original data I'm working with is Corn data, from 1972->2011.
       Only 2 digits are stored for year.
    """
    month, day, year = int(datamine_date[0:2]), int(datamine_date[2:4]), int(datamine_date[4:6])
    if year in range(72,100):
        year = 1900 + year
    else:
        year = 2000 + year
    return datetime.date(year, month, day)

def get_expiration(fut_option_indicator, exp_year, exp_month):
    """CME doesn't give expiration day; they set day == 0 for non-daily options"""
    # TODO:get real expiration days
    # for now, just give back the 20th of the month every month
    exp_year = int(exp_year)
    exp_month = int(exp_month)
    return datetime.date(exp_year, exp_month, 20)

def parse_cme_row(row):
    (trade_date,product_symbol,C,fut_opt_indicator,exp_month,exp_day,exp_year,strike,I,px_open,K,L,M,px_high,O,px_low,Q,px_close,S,T,U,px_settle,volume,open_interest,Y,imp_volatility,AA) = row.split(",")
    # The garbage fields in this tuple are just alphabetical corresponding to the excel column number as defined in the CME spec.
    # I didn't want them so didn't want to waste chars.
    # px_last = px_close # really?
    # The historical data defines Open-High-Low-CLOSE data
    # The daily settlements have an Open-High-Low-LAST.
    # These are probably the same thing, but leave note for clarity later.
    formatted_row = [datamine_date_to_datetime(trade_date),
                     product_symbol,
                     fut_opt_indicator,
                     get_expiration(fut_opt_indicator, exp_year, exp_month),
                     float(strike),
                     float(px_open),
                     float(px_high),
                     float(px_low),
                     float(px_close),
                     float(px_settle),
                     float(volume),
                     float(imp_volatility),
                    ]
    return formatted_row

cme_sample_row = "010311,PY,R,P,12,0,2012,450.0000000,,.0000000,,.0000000,,.00000000,,.00000000,N,501.00000000,,.00000000,,524.00000000,.0000000,108.000000,0,.306303,CBT"

if __name__ == "__main__":
    source_csv = "Corn.csv"
    dbname = "filteredcornDB.sqlite3"
    conn = open_db(dbname)
    headers = ["trade_date date",
               "product_symbol",
               "fut_opt_indicator",
               "exp_date date",
               "strike",
               "px_open",
               "px_high",
               "px_low",
               "px_close",
               "px_settle",
               "volume",
               "imp_volatility",
              ]
    tables = ["Futures", "Options"]
    for table in tables:
        create_table_if_not_exists(conn, tablename=table, schema=", ".join(headers))

    headers = ["trade_date",
               "product_symbol",
               "fut_opt_indicator",
               "exp_date",
               "strike",
               "px_open",
               "px_high",
               "px_low",
               "px_close",
               "px_settle",
               "volume",
               "imp_volatility",
              ]
    with open(source_csv, "r") as f:
        rows = f.readlines()
        for r in rows:
            # some filters, determiend by trial and error
            if rows[2] == "E":
                # E == electronic, R == pit.  Electronic values are garbage for close.
                continue



            values = parse_cme_row(r)
            if values[1] == "C":
                #Future
                insert_record(conn, "Futures", headers, values)
            elif values[1] == "PY":
                #Option
                insert_record(conn, "Options", headers, values)
            else:
                # 8CC and CCZ
                pass
    conn.commit()
    conn.cursor().close()
