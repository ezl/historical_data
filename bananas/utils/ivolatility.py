import pymssql
from random_shit import multiple_key_delete

host = 'rock340:1948'
user = 'Rock357'
password = 'the$r0ck357'
database = 'IVolatility'

def query(sql, as_dict=False):
    conn = pymssql.connect(host=host, user=user, password=password,
                       database=database)
    cur = conn.cursor()
    cur.execute(sql)
    columns = tuple(x[0] for x in cur.description)
    if as_dict:
        results = cur.fetchall_asdict()
        # for some shitty reason the dict returns data twice. lets clean it.
        numeric_keys = len(results[0])
        for r in results:
            multiple_key_delete(r, range(numeric_keys))
    else:
        results = cur.fetchall()
    conn.close()
    return columns, results

