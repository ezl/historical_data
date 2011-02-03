#OC: mysql -h10.51.132.92 -ueric -pziu

import time
import datetime
import os
import sqlite3

def open_db(dbname="DB.sqlite3"):
    if not os.path.isfile(dbname):
        print "SQLite database %s does not exist. Creating it." % dbname
        # raise Exception, "SQLite database %s does not exist."
    conn = sqlite3.connect(dbname)
    return conn

def create_table_if_not_exists(conn, tablename="TEST", schema=None):
    """Wrapper for SQLite's conditional table creation.

       If table does not exist, create it.

       In future, consider implementing:
           If table exists, but the schema does not match specification, Exception.
           If table exists, and schema matches, do nothing.

       The schema parameter is a dictionary with "key/value" pairs like:
           schema = dict(quantity="INTEGER",
                         underlying="VARCHAR",
                         symbol="VARCHAR",
                         actype="VARCHAR",
                         porc="VARCHAR(1)",
                         exchange="VARCHAR(10)",
                         actdate="TIMESTAMP",
                        )

       OR a string like:
           schema = 'quantity INTEGER,
                     underlying VARCHAR,
                     symbol VARCHAR,
                     actype VARCHAR,
                     porc VARCHAR(1),
                     exchange VARCHAR(10),
                     actdate TIMESTAMP)
                    '
    """
    schema = dict(quantity="INTEGER",
                  underlying="VARCHAR",
                  symbol="VARCHAR",
                  actype="VARCHAR",
                  porc="VARCHAR(1)",
                  exchange="VARCHAR(10)",
                  actdate="TIMESTAMP",
                 )
    if isinstance(schema, dict):
        schema_string = ", ".join(["%s %s" % (k, v) for (k, v) in schema.items()])
    elif isinstance(schema, str):
        schema_string = schema
    else:
        raise Exception, "Unable to determine schema for table creation"
    sql = """CREATE TABLE IF NOT EXISTS %s (%s)""" % (tablename, schema_string)
    conn.cursor().execute(sql)

def insert_record(conn, tablename, headers, values):
    """headers and values are lists"""
    sql = """INSERT INTO %s(%s) VALUES (%s)""" % (tablename, ", ".join(headers), ", ".join(["?",] * len(values)))
    conn.cursor().execute(sql, values)

def insert_csv_to_sqlite3(conn, fields, content, data_has_headers=False):
    """GENERALIZED csv -> sqlite3 insertion. WIP.

       Inputs:
           conn: db connection to sqlite3 file.
           fields: the table fields to insert data to.
           content: Huge csv string.  Rows are separated by newline ("\n").
           data_has_headers: Does the content block have a header row?
                             If False, the first row will be used;
                             if True, the first row will be discarded.
       Outputs:
           returns None.  Will raise Exception on error.

    """
    rows = content.strip().split("\n")
    if data_has_headers:
        rows.pop(0)
    if not len(rows) > 0:
        # TODO:This could behave oddly if a large data set has no "\n" separators.
        print "No data found."
        return
    data = [entry.strip().split(",") for entry in rows]

    # Time conversion. Ugh Garbage. This method sucks.
    # Method will be fine for dumping RAW csvs to sqlite, but if you want to format
    # times or any data before entry, must do individual entry with insert_record()
    for entry in data:
        timeformat = time.strptime(entry[-1], "%m/%d/%Y")
        entry[-1] = datetime.date(*timeformat[:3])

    sql = """INSERT INTO occ(quantity, underlying, symbol, actype, porc, exchange, actdate) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    conn.cursor().executemany(sql, data)

if __name__ == "__main__":
    conn = open_db()
    create_table_if_not_exists(conn, tablename="TEST")
    headers = ["quantity", "underlying", "symbol", "actype", "porc", "exchange", "actdate"]
    values = [10, 1310.2, "SPX", "Customer", "C", "CBOE", datetime.date(2011,7,22)]
    tablename = "TEST"
    insert_record(conn, tablename, headers, values)
    conn.commit() # close db
    conn.cursor().close()
