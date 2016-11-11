# -*- coding: utf-8 -*-


from RestfulCaseManager.Model.Paramter import *

class HistoryManager:
    def __init__(self):
        self.assessDB = MongodbOperation.getMongodb()
        if self.assessDB == None:
            self.testcases = None
            self.result =  None
            self.module =  None
        else:
            self.testcases = self.assessDB["testcases"]
            self.result = self.assessDB["result_case"]
            self.module = self.assessDB["module"]


    def findLatestRunResultListById(caseid):
        return

    def findLatestLatestRespnseListById(caseid):





        return

    def getCaseIdList(caseList):
        caseIdList = []
        if caseList:
            for case in caseList:
                print case['_id']
                caseIdList.append(case['_id'])

        return caseIdList
