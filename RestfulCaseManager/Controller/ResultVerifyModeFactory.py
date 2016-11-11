# coding = utf-8

from jsonpath_rw import jsonpath, parse
import json

# use simple factory pattern
class VerifyModeBase():
    def __init__(self,case):
        self.case = case

    def setActualResult(self):
        pass

class CodeVerifyMode(VerifyModeBase):
    def __init__(self,case):
        VerifyModeBase.__init__(self,case)

    def setActualResult(self):
        self.case.actualResult =  self.case.code

class FullMatchVerifyMode(VerifyModeBase):
    def __init__(self,case):
        VerifyModeBase.__init__(self,case)

    def setActualResult(self):
        # self.case.actualResult = self.case.responseContent

        if self.case.responseContent_json:
            self.case.actualResult = json.dumps(self.case.responseContent_json)
        else:
            self.case.actualResult = ""

class JsonPathVerifyMode(VerifyModeBase):
    def __init__(self,case):
        VerifyModeBase.__init__(self,case)

    def setActualResult(self):
        jsonpath_expr = parse(self.case.jsonPath)
        match = jsonpath_expr.find(self.case.responseContent_json)
        if len(match) > 0:
            self.case.actualResult = match[0].value
        else:
            self.case.actualResult = ""


class VerifyModeFactory(object):
    # Create based on class name:
    @staticmethod
    def factory(case):
        if case.verifyMode.lower() == "code":
            return CodeVerifyMode(case)
        elif case.verifyMode.lower() == "jsonpath":

            return JsonPathVerifyMode(case)
        else:
            return FullMatchVerifyMode(case)

'''
class Test():
    def __init__(self,name,group,requestType,url,data,verifyMode,expectedResult,jsonPath):
        self.name = name
        self.group = group
        self.requestType = requestType
        self.url = url
        self.data = data
        self.verifyMode = verifyMode
        self.expectedResult = expectedResult
        self.response =  None
        self.result = "none"
        self.responseStatus = ""
        self.responseContent_json = ""
        self.jsonPath = jsonPath
        self.session = ""


    def printName(self):
        print self.name

case = Test("name","group","get","url",{},"Code","200","$.data.section2")
case.code = "200"
case.responseContent_json = {"code":200,"data":{"section1":"qqq","section2":"wwww"}}
case.responseContent = str(case.responseContent_json)
aaa = VerifyModeFactory.factory("2222",case)
print aaa.setActualResult()
print "dddd:",aaa.case.actualResult
'''





