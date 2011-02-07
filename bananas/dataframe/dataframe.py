import numpy as np

class dataframe(object):
    def __init__(self, columns, data):
        self.columns = columns
        self.column_key = dict()
        self.data = list()
        for i, column in enumerate(columns):
            self.column_key[column] = i
            self.data.append(np.array([row[i] for row in data]))
    def __repr__(self):
        if self.numrows() == 0:
            return "Dataframe is empty."
        columns = str(self.columns)
        first_row = str([field[0] for field in self.data])
        repr = """
Columns: %s
First row: %s
""" % (columns, first_row)
        return repr
    def __call__(self, *columns):
        if len(columns) == 0:
            return self.data
        elif len(columns) == 1:
            return self.data[self.column_key[columns[0]]]
        else:
            return np.array([self.data[self.column_key[c]] for c in columns]).transpose()
    def numcols(self):
        return len(self.columns)
    def numrows(self):
        return len(self.data[0])
    def update(self, column, values, index=None):
        if index is None:
            index = range(self.numrows())
        self.data[index, self.column_key[column]] = values

def execute_query_DF(conn, query):
    cur=conn.cursor()
    cur.execute(query)
    columns=[x[0] for x in cur.description]
    data = cur.fetchall()
    cur.close()
    return dataframe(columns, data)
