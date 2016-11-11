# encoding='utf-8'
from RestfulCaseManager.util.DBOracleOpration import DatabaseOperation
from RestfulCaseManager.util import ConfigReader


class CaseEnder():
    def __init__(self,module, env):
        conf = ConfigReader.read_conf(module)
        self.db_oracle_username = conf.get(env,"db_oracle_username")
        self.db_oracle_password = conf.get(env,"db_oracle_password")
        self.db_oracle_host = conf.get(env,"db_oracle_host")
        self.oracle_connecton = DatabaseOperation(self.db_oracle_username, self.db_oracle_password, self.db_oracle_host)

    def deleteAllData(self):
        self.deleteLiuweiData()

    def deleteLiuweiData(self):
        args = [{'person_id':378030}]
        sqlDeleteLiuweiData = "delete from hcm.CUX_MT_SIX_DIMENSION where person_id  = :person_id"
        self.oracle_connecton.executemany(sqlDeleteLiuweiData,args=args)
    pass

