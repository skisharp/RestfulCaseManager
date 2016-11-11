import cx_Oracle

class DatabaseOperation():

    def __init__(self, username, passoword, host):
        self.conn = self.getOracleConnection(username, passoword, host)
        self.cursor = self.conn.cursor()

    def getOracleConnection(self,username, passoword, host):
        # con = cx_Oracle.connect('polar', 'polardev5', 'tc-erp-devdb05.tc:8055/PLDEV5')
        conn = cx_Oracle.connect(username, passoword,host)
        return conn

    def executemany(self,sql,args):
        # http://www.oracle.com/technetwork/articles/dsl/prez-python-queries-101587.html
        # http://www.oracle.com/webfolder/technetwork/tutorials/obe/db/oow10/python_db/python_db.htm
        # args = [{'person_id':378030}]
        # cursor.executemany("delete from hcm.CUX_MT_SIX_DIMENSION where person_id  = :person_id", named_params)
        self.cursor.executemany(sql, args)
        self.conn.commit()

    def executeQuery(self,sql,args):
        # sql = 'select * from hcm.CUX_MT_SIX_DIMENSION where person_id  = 378030'
        self.cursor.execute(sql)
        for row in self.cursor:
            print row

    def close(self):
        self.conn.close()


