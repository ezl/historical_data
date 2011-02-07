import numpy as np

def executeQueryDF(conn, query, params=None):
    cur=conn.cursor()
    if params is None:
        cur.execute(query)
    else:
        cur.execute(query, params)
        
    columns=[x[0] for x in cur.description]
    data = np.array(cur.fetchall(),'object')
    cur.close()
    return dataframe([columns,data])

class dataframe(list):
    def __init__(self, *args):
        if len(args) == 2:
            [colnames,arraydata]=args
        else:
            [colnames,arraydata]=args[0]
            
        list.__init__(self)
        self.append(colnames)
        if arraydata is None:
            arraydata = np.empty((0, len(colnames))).astype('object')
        self.append(arraydata)
        self.cdict={}
        for i,cname in enumerate(colnames):
            self.cdict[cname]=i
            
    def g(self, colname):
        if isinstance(colname,list):
            return [self.gsingle(x) for x in colname]
        else:
            return self.gsingle(colname)
    def ga(self,colname):
        if isinstance(colname,list):
            colidx=np.array([self.cdict[x] for x in colname])
            return self[1][:,colidx]
        else:
            return self.g(colname)
    def s(self, colname, val, idx=None):
        if idx is None:
            idx=np.arange(0,self.numrows())
        if isinstance(colname, list):
            colidx=np.array([self.cdict[x] for x in colname])
            self[1][idx,colidx]=val
        else:
            colidx=self.cdict[colname]
            self[1][idx,colidx]=val
            
    def add(self,colname,col):
        self[0].append(colname)
        self[1]=np.column_stack((self[1], col))
        self.cdict[colname]=self.numcols()-1
        
    def gsingle(self,colname):
        return self[1][:,self.cdict[colname]]
    
    def numcols(self):
        return len(self[0])
    
    def numrows(self):
        return(self[1].shape[0])
    
    def data(self):
        return(self[1])
    
    def cols(self):
        return(self[0])
    
    def set_data(self, data):
        self[1] = data


