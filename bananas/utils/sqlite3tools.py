import sqlite3
from datetime import datetime

def insert_to_sqlite(conn, tablename, columns, results):
    '''
    tablename is string; columns, results are tuple

    creates table if it doesn't already exist.
    '''
    create_sqlite_table(conn=conn, tablename=tablename, columns=columns)
    column_names_string = str(columns).replace("'","")
    question_marks_string = str(tuple(["?" for c in columns])).replace("'","")
    SQL_insert = "INSERT INTO %s %s VALUES %s" % (tablename,
                                                  column_names_string,
                                                  question_marks_string)
    # conn.cursor().executemany(SQL_insert, results)
    conn.cursor().execute(SQL_insert, results)
    conn.commit()

def create_sqlite_table(conn, tablename, columns):
    column_names_string = str(columns).replace("'","")
    conn.execute("CREATE TABLE IF NOT EXISTS %s %s" % (tablename,
                                                       column_names_string))

def delete_sqlite_table(conn, tablename):
    conn.execute("DROP TABLE IF EXISTS %s" % tablename)

def convert_to_epoch_times(conn, table, column):
    SQL_convert = """
    UPDATE %(table)s SET %(column)s=strftime('%%s', %(column)s, 'utc')
    """ % {"table":table, "column":column}
    conn.execute(SQL_convert)
    conn.commit()

