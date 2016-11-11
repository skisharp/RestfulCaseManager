# -*- coding: utf-8 -*-
import traceback
import logging
import pymongo
import types
# 在mongodb中id的class
from bson.objectid import ObjectId

from RestfulCaseManager.Model.TestcaseBase import *

from RestfulCaseManager.Model.Paramter import *
from RestfulCaseManager.util import ConfigReader

import ResultVerifyModeFactory
from RestfulCaseManager.Model.CaseRunningLogString import RunningLogString
from RestfulCaseManager.util import FileOperation


class CaseManager(object):

    caseList = []

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

    # 得到所有模块
    def getModules(self):
        return self.module.find()

    # 得到Priority
    def getPriorityList(self):
        return ["P0", "P1", "P2", "P3"]

    # 得到http 请求方式
    def getRequestTypeList(self):
        return ["Post", "Get", "Put"]

    # 得到结果验证模式
    def getVerifyModeList(self):
        return ["jsonPath", "code", "fullMatch", "sql"]

    # 获取case列表
    # module 模块
    # order 根据添加时间进行倒序
    def getCaseList(self, module='test', order="addTime", start_index=1):
        try:
            self.caseList = self.testcases.find({'module': module}).sort(order, pymongo.DESCENDING).limit(5).skip(start_index)
        except:
            logging.exception("Error:")

        return self.caseList

    # 添加测试用例到DB
    def addCase(self, postData):
        try:
            post_id = self.testcases.insert(postData)
            logging.info("添加测试用例数据：")
            logging.info(postData)
        except Exception,e:
            logging.exception("Error:")

    # 删除case caseId case 的id
    def delete_case(self, case_id):
        object_id = ObjectId(case_id)
        try:
            self.testcases.remove({"_id": object_id})
        except Exception:
            logging.exception("Error:")
        return self.caseList

    # 通过id查询case
    def getCaseById(self, caseId):
        objectId = ObjectId(caseId)
        try:
            case = self.testcases.find_one({"_id": objectId})
        except Exception,e:
            logging.exception("Error:")
        return case

    # 更新case到DB
    def updateCase(self, caseId, postData):
        objectId = ObjectId(caseId)
        try:
            case = self.testcases.update_one(
                {"_id": objectId},
                {"$set":{
                    "name": postData["name"],
                    "url": postData["url"],
                    "data": postData["data"],
                    "requestType": postData["requestType"],
                    "expectedResult": postData["expectedResult"],
                    "verifyMode": postData["verifyMode"],
                    "jsonPath": postData["jsonPath"],
                    "module": postData["module"],
                    "priority": postData["priority"],
                    "role": postData["role"],
                    "comment": postData["comment"]
                    }
                 }
            )

        except Exception,e:
            logging.exception("更新测试用例失败：")

    # 1 运行测试用例setup
    def setUp(self, module, env):
        RunningLogString.logString = RunningLogString.logString + 'Init 开始' + '<br/>'
        logging.info('Init 开始**************************')

        path_module_path =  FileOperation.get_module_file_dir(module=module)
        RunningLogString.logString = RunningLogString.logString + 'Init 文件路径：' + path_module_path + '<br/>'

        sys.path.insert(0, path_module_path)
        CaseInitModule = __import__('CaseInit')
        CaseInitClass = CaseInitModule.CaseInit()
        self.restRequest = CaseInitClass.initCase(module, env)
        RunningLogString.logString = RunningLogString.logString + 'Init 结束'+ '<br/>'

    # 2 运行测试用例
    def run(self, module='test', env='8030', caseId=""):
        self.conf = ConfigReader.read_conf(module)
        #   得到测试用例列表
        if caseId == "":
            caseObjectList = self.getCaseObject(module)
        else:
            caseObjectList = self.getCaseObject(caseId=caseId)

        self.domain = self.conf.get(env, "domain")

        # 执行测试用例
        response = ""
        from bson.objectid import ObjectId
        batch_id = ObjectId()

        for item in caseObjectList:
            RunningLogString.logString = ''
            runStartTime = datetime.datetime.now()
            RunningLogString.logString = RunningLogString.logString + '=============开始执行:'
            RunningLogString.logString = RunningLogString.logString + runStartTime.strftime('%c') + '<br/>'
            RunningLogString.logString = RunningLogString.logString + '测试用例名称：'
            RunningLogString.logString = RunningLogString.logString + item.name + '<br>'
            logging.info('=============开始执行:')
            logging.info('测试用例名称：')
            logging.info(item.name)
            logging.info(item.url)

            try:
                item.run_case(module=module)
                if not item.response:
                    item.actualResult = ''
                    item.response = None
                    item.result = 'Fail'
                    item.responseStatus = '0000'
                    item.runningTime = ''
                    item.loggingString = RunningLogString.logString
                    self.saveResultToDB(item, batch_id)
                    logging.info("response is nones")
                    RunningLogString.logString = RunningLogString.logString + "运行结果：None<br/>"
                    continue
                logging.info(item.response.content)
                RunningLogString.logString = RunningLogString.logString + "运行结果：" + item.response.content + '<br/>'

                # item.response.text type unicode
                # item.response.content type str
                item.responseStatus = item.response.status_code
                item.responseContent = item.response.content

                if item.responseContent != "":
                    try:
                        item.responseContent_json = json.loads(item.responseContent)
                        item.code = item.responseContent_json["code"]
                    except:
                        item.code = ""
            except:
                RunningLogString.logString = RunningLogString.logString + "运行异常"
                logging.exception("出现异常：")
            logging.info('得到结果')
            verifyModeClass = ResultVerifyModeFactory.VerifyModeFactory.factory(item)
            verifyModeClass.setActualResult()

            if type(item.actualResult) is int:
                if str(item.actualResult) == str(item.expectedResult):
                    item.result = "Pass"
            elif str(item.actualResult.encode("utf-8")) == str(item.expectedResult):
                item.result = "Pass"
            else:
                item.result = "Fail"

            logging.info("运行结束")

            runRndTime = datetime.datetime.now()
            runTime = runRndTime -  runStartTime
            runTimeMicroseconds = runTime.microseconds
            runTimeSeconds = runTimeMicroseconds / 1000.0
            item.runningTime = runTimeSeconds

            RunningLogString.logString = RunningLogString.logString + "============运行结束："
            RunningLogString.logString = RunningLogString.logString + runRndTime.strftime('%c') + '<br/>'

            item.loggingString = RunningLogString.logString

            # 保存运行结果
            self.saveResultToDB(item, batch_id)

        return {"caseObjectList": caseObjectList, "batch_id": batch_id}

    # 3 tear down
    def tearDown(self, module, env):
        RunningLogString.logString = RunningLogString.logString + "============开始运行Teardown============" + '<br/>'
        CaseEnderModule = __import__('CaseEnder')
        CaseEnderClass = CaseEnderModule.CaseEnder(module, env)
        CaseEnderClass.deleteAllData()
        RunningLogString.logString = RunningLogString.logString + "============运行Teardown结束===========" + '<br/>'

    # 执行case 主函数
    def runCase(self, module="Mtool", env="8030", caseId=""):
        self.successCaseObjectList  = []
        self.failCaseObjectList = []

        RunningLogString.logString = ''
        result = None
        try:
            logging.info("=============init================")
            self.setUp(module, env)
            logging.info("=============init  End================")
            logging.info("=============start 运行测试用例================")
            if caseId == "":
                result = self.run(module, env)
            else:
                result = self.run(caseId=caseId, env=env, module=module)
            logging.info("=============running end================")
            logging.info("=============teardown start================")
            self.tearDown(module, env)
            logging.info("=============teardown end================")
        except:
            logging.exception("Error:")

        return result

    #  获取测试用例Object列表
    def getCaseObject(self, module = "Mtool", caseId = ""):
        logging.info("开始获取case列表")
        paramter = Paramter(module)
        paramObjectList = paramter.getParameterObject(module)
        if caseId == "":
            caseList = self.testcases.find({"module": module})
        else:
            objectId = ObjectId(caseId)
            caseList = self.testcases.find({"_id": objectId})

        caseObjectList = []
        for case in caseList:
            name = case["name"].encode("utf-8")
            url = case["url"].encode("utf-8")
            caseId = case["_id"]
            requestType = case["requestType"].encode("utf-8")
            # data = case["data"].encode("utf-8")
            data = case["data"]
            # 结果有两种格式，string和dict
            # expectResult = case["expectedResult"].encode("utf-8")
            expectResult = case["expectedResult"]
            verifyMode = case["verifyMode"].encode("utf-8")
            jsonPath = case["jsonPath"].encode("utf-8")
            role = case["role"].encode("utf-8")
            module = case["module"].encode("utf-8")
            caseObject = TestcaseBase(name,url,requestType,data,verifyMode,expectResult,jsonPath,role,module)
            caseObject.setId(caseId)

            caseObjectList.append(caseObject)

        logging.info("参数列表：")
        logging.info(paramObjectList)

        for item in caseObjectList:
            if '$date_year_month_day' in item.data:
                import datetime
                now_year_month_day = datetime.datetime.now().strftime('%Y-%m-%d')
                item.data = item.data.replace('$date_year_month_day', now_year_month_day)
            for param in paramObjectList:
                logging.info(param.name + param.value)
                try:
                    item.data = item.data.replace(param.name, param.value)
                except:
                    logging.exception("替换参数出现异常：")
                    break

        logging.info("获取case列表成功")

        return caseObjectList

    # 存储执行结果到result
    def saveResultToDB(self, item, batch_id):
        response_content = ''
        if item.response:
            response_content = item.response.content

        result = {
                "caseId": item.caseId,
                "caseName": item.name,
                "result": item.result,
                "responseCode": item.responseStatus,
                "response": response_content,
                "actualResult": item.actualResult,
                "runningDate": datetime.datetime.now().strftime('%c'),
                "runningTime": item.runningTime,
                "batch_id": batch_id,
                "loggingString": item.loggingString
                }
        try:
            resultObjectId = self.result.insert(result)
            item.resultObjectId = resultObjectId
        except:
            logging.exception("保存运行结果出错：")
        finally:
            return batch_id


    # 得到运行的结果
    def get_result(self, batch_id):
        batch_id = ObjectId(batch_id)
        try:
            result_list = self.result.find({"batch_id": batch_id}).sort("runningDate", pymongo.DESCENDING)
        except:
            logging.error(traceback.print_exc())
        return result_list

    # 得到一个测试用例的历史结果
    def getHistoryResult(self, caseId):
        objectId = ObjectId(caseId)
        try:
            resultList = self.result.find({"caseId": objectId}).sort("runningDate", pymongo.DESCENDING)
        except Exception,e:
            logging.error(traceback.print_exc())
        return resultList

    # 得到一个测试用例日志
    def get_result_logging(self, case_id):
        if isinstance(type(case_id), types.UnicodeType):
            case_id = ObjectId(case_id)
        log = ''
        try:
            log = self.result.find_one({"_id": case_id})["loggingString"].encode('utf-8')
        except Exception:
            logging.exception("出现异常：")
            log = '从数据库获取日志出现异常！'
        return log

    # # 导入case到DB
    # def importCaseToDB(self, case_json):
    #     try:
    #         caseList = case_json['testcases']
    #         for case in caseList:
    #             self.testcases.insert(case)
    #     except :
    #         logging.exception("Error:")
    #     return self.caseList


    # 导出case到json文件
    # def exportCasesToFile333(self):
    #     try:
    #         self.caseList = self.testcases.find()
    #         test = '{"testcases":['
    #         for case in self.caseList:
    #             test = test + '{'
    #             test = test + '"name":' + '"' + case["name"] + '",'
    #             test = test + '"url":' + '"' + case["url"] + '",'
    #             test = test + '"RequestMethod":' + '"' + case["requestType"] + '",'
    #             if case["data"]:
    #                 test = test + '"data":' + case["data"] + ','
    #             else:
    #                 test = test + '"data":{},'
    #             test = test + '"ExpectedResult":' + '"' + case["expectedResult"] + '",'
    #             test = test + '"VerifyMode":' + '"' + case["verifyMode"] + '",'
    #             test = test + '"JsonPath":' + '"' + case["jsonPath"] + '",'
    #             test = test + '"Priorith":' + '"' + case["priority"] + '",'
    #             test = test + '"Module":' + '"' + case["module"] + '",'
    #             test = test + '"Comment":' + '"' + case["comment"] + '"'
    #             test = test + '},'
    #         test = test + ']}'
    #
    #     except Exception,e:
    #         logging.exception("Error:")
    #     with open('test.json', 'w') as f:
    #         reload(sys)
    #         sys.setdefaultencoding('utf-8')
    #         f.write(test)
    #     return "success!"

        # # 导出case到json文件
    # def exportCasesToFile(self):
    #
    #     try:
    #         self.caseList = self.testcases.find()
    #         test = {"testcases":[]}
    #         for case in self.caseList:
    #             caseDict = {
    #                 "name":case["name"].encode("utf-8"),
    #                 "url":case["url"],
    #                 "RequestMethod":case["requestType"],
    #                 "data":case["data"],
    #                 "ExpectedResult":case["expectedResult"],
    #                 "VerifyMode":case["verifyMode"],
    #                 "JsonPath":case["jsonPath"],
    #                 "Priorith":case["priority"],
    #                 "Module":case["module"],
    #                 "Comment":case["comment"]
    #             }
    #             test["testcases"].append(caseDict)
    #
    #     except Exception,e:
    #         logging.exception("Error:")
    #     with open('test.json', 'w') as f:
    #         reload(sys)
    #         sys.setdefaultencoding('utf-8')
    #         f.write(json.dumps(test,ensure_ascii=False,indent=4,sort_keys=False,encoding='utf-8'))
    #     return "success!"









