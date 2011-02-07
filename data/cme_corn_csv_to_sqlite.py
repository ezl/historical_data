from bananas.db.sqliteutils import open_db, create_table_if_not_exists, insert_record

if __name__ == "__main__":
    """Dump the total CME corn datamine csv into a big sqlite file"""

    cme_csv = "Corn.csv"
    dbname = "cornDB.sqlite3"
    # CME Group End-of-Day Record Layout Guide (CSV format)
    # source: http://www.cmegroup.com/market-data/datamine-historical-data/files/EODLayoutGuideCSV.pdf
    headers = ["trade_date",
               "product_symbol",
               "trade_session",
               "future_option_indicator",
               "expiration_month",
               "expiration_day",
               "expiration_year",
               "strike_price",
               "open_ask_bid_indicator",
               "open_price",
               "opening_range_ask_bid_indicator",
               "opening_range",
               "high_ask_bid_indicator",
               "high_price",
               "low_ask_bid_indicator",
               "low_price",
               "close_ask_bid_indicator",
               "close_price",
               "closing_range_ask_bid_indicator",
               "closing_range",
               "settle_cabinet",
               "settle_price",
               "actual_volume",
               "open_interest",
               "option_exercises",
               "implied_volatility",
               "exchange",
              ]
    tablename = "CME"
    conn = open_db(dbname)
    create_table_if_not_exists(conn, tablename=tablename, schema=", ".join(headers))
    with open(cme_csv, "r") as f:
        rows = f.readlines()
        for row in rows:
            insert_record(conn, tablename, headers, row.split(","))
    conn.commit()
    conn.cursor().close()
