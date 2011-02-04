#OC: mysql -h10.51.132.92 -ueric -pziu

import time
import datetime
import os
import sqlite3

def open_db(dbname=None):
    if not os.path.isfile(dbname):
        pass
        # print "SQLite database %s does not exist. Creating it." % dbname
        # raise Exception, "SQLite database %s does not exist."
    conn = sqlite3.connect(dbname)
    return conn

def create_table_if_not_exists(conn, tablename, schema):
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
    if isinstance(schema, dict):
        schema_string = ", ".join(["%s %s" % (k, v) for (k, v) in schema.items()])
        # sqlite doesn't require or use types, so the dict method is really pointless.
    elif isinstance(schema, str):
        schema_string = schema
    else:
        raise Exception, "Unable to determine schema for table creation"
    sql = """CREATE TABLE IF NOT EXISTS %s (%s)""" % (tablename, schema_string)
    conn.cursor().execute(sql)
    return None

def insert_record(conn, tablename, headers, values):
    """Insert a record.

       Inputs: headers and values are lists
       Note, this uses %s for string substitution which is considered insecure and susceptible to
       SQL injection attacks.  For internal use only, so not optimizing for flexibility instead
       by using bad practice.
    """
    sql = """INSERT INTO %s(%s) VALUES (%s)""" % (tablename, ", ".join(headers), ", ".join(["?",] * len(values)))
    conn.cursor().execute(sql, values)
    return None

if __name__ == "__main__":
    """Example usage"""
    conn = open_db("TESTDB.sqlite3")
    headers = ["quantity", "underlying", "symbol", "actype", "porc", "exchange", "actdate"]
    values = [10, 1310.2, "SPX", "Customer", "C", "CBOE", datetime.date(2011,7,22)]
    tablename = "TEST"
    create_table_if_not_exists(conn, tablename="TEST", schema=", ".join(headers))
    insert_record(conn, tablename, headers, values)
    conn.commit() # close db
    conn.cursor().close()
