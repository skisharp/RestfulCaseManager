# coding: utf-8

from RestfulCaseManager.util import MongodbOperation


class Paramter():
    def __init__(self,name = "", val = "", method = "", module = ""):
        self.name = name
        self.value = val
        self.method = method
        self.module = module

    def addParamter(self):

        MtoolDB = MongodbOperation.getMongodb()
        paramters_table =  MtoolDB["paramters"]
        parameter_temp = {
             "name":self.name,
            "value" : self.value,
            "method" : self.method,
            "module" : self.module
        }

        paramters_table.insert(parameter_temp)


    def getParameters(self,module = "Mtool"):
        MtoolDB = MongodbOperation.getMongodb()
        paramters_table =  MtoolDB["paramters"]
        paramterList = paramters_table.find({"module":module})

        return  paramterList

    def getParameterObject(self,module = "Mtool"):
        paramObjectList = []
        paramterList = self.getParameters(module)

        print module
        for param in paramterList:
            paramObject  = Paramter(param["name"],param["value"],param["method"],param["module"])
            paramObjectList.append(paramObject)
        return  paramObjectList





