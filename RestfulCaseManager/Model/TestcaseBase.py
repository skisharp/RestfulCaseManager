# coding=utf-8
__author__ = 'zhangruixia'

import json
import datetime
import os
import logging

from jsonpath_rw import parse

from RestfulCaseManager.Controller import RestRequest
from RestfulCaseManager.Model import  Env
import sys
# 日志信息
from RestfulCaseManager.Model.CaseRunningLogString import RunningLogString
from RestfulCaseManager.Controller import RoleUserMapper



# 测试用例 class
class TestcaseBase:
    def __init__(self,name,url,requestType,data,verifyMode,expectedResult,jsonPath,role,module):
        self.name = name
        self.url = url
        self.data = data
        self.requestType = requestType
        # 验证模式 json sql
        self.verifyMode = verifyMode
        self.expectedResult = expectedResult
        self.jsonPath = jsonPath
        # 角色
        self.role = role
        self.module = module
        self.response = None
        self.result = "none"
        self.responseStatus = ""
        self.responseContent_json = ""
        # 记录结果ID
        self.resultObjectId = None

    # case id
    def setId(self, caseId):
        self.caseId = caseId

    # 运行测试用例
    def run_case(self, module, env):
        print("begin run case, module = " + module)
        running_flag = True

        # 1 登录erp
        loginSession = self.loginERP(module=module, env=env)
        if loginSession is None:
            RunningLogString.logString = RunningLogString.logString + "登录失败"
            return running_flag

        self.restRequest = RestRequest.RestRequest(loginSession)

        # 拼接url
        url_temp = Env.Env.domain + self.url
        RunningLogString.logString = RunningLogString.logString + "URL：" + url_temp + '<br/>'
        RunningLogString.logString = RunningLogString.logString + "数据：" + self.data.encode('utf-8') + '<br/>'
        RunningLogString.logString = RunningLogString.logString + "请求方法：" + self.requestType.encode('utf-8') + '<br/>'

        # TODO:simple
        if self.requestType == "Get":
            self.response = self.restRequest.restGet(url_temp)
        elif self.requestType == "Put":
            json_data = json.loads(self.data)
            self.response = self.restRequest.restPut(url_temp, data=json_data, params=None)
        else:
            json_data = json.loads(self.data)
            self.response = self.restRequest.restPost(url_temp, data=json_data, params=None)
            testabc = self.restRequest.restPost(url_temp, data=json_data, params=None)

        if self.response is None:
            self.responseStatus = '000'
            self.responseContent = ''
            self.responseContent_json = ''
            self.code = ''
            RunningLogString.logString = RunningLogString.logString + "请求结果 is none'<br/>"
        else:
            self.responseStatus = self.response.status_code
            self.responseContent = self.response.content
            if self.responseContent != "":
                try:
                    self.responseContent_json = json.loads(self.responseContent)
                    self.code = self.responseContent_json["code"]
                except:
                    self.code = ""
                    import logging
                    logging.exception("存储responseContent_json报错")
            else:
                self.code = ''
                self.responseContent_json = ''

    # erp登录
    # 登录来获取session 和
    # RestRequest
    def loginERP(self, module, env):
        '''
        :param module: ERP模块
        :param env: ERP运行环境：8030，8020，8010 .。。
        :return:
        '''
        # self.loginSession = loginERP.login(self.loginDomain,self.user,self.user + self.passwordpostfix)
        # self.restRequest = RestRequest(self.loginSession)
        RunningLogString.logString = RunningLogString.logString + "开始登录ERP<br/>"

        configDir = os.path.join(os.getcwd(), "RestfulCaseManager")
        configDir = os.path.join(configDir, "CaseFiles")
        pathCase = os.path.join(configDir, self.module)
        RunningLogString.logString = RunningLogString.logString + "登录文件路径:" + pathCase+ '<br/>'
        sys.path.insert(0, pathCase)

        loginERPModule = __import__('loginERP')

        # 根据角色获取用户名和密码
        RoleUserMapper.RoleUserMapper.getRoleUserDict(module)
        user = RoleUserMapper.RoleUserMapper.roleUserJson.get(self.role)

        #RunningLogString.logString = RunningLogString.logString + "登录角色:" + self.role.encode('utf-8')+ '<br/>'
        #RunningLogString.logString = RunningLogString.logString + "登录用户名:" + user.encode('utf-8') + '<br/>'
        #RunningLogString.logString = RunningLogString.logString + "登录密码:" + (user + Env.Env.passwordpostfix).encode('utf-8') + '<br/>'
        loginSession = None
        try:
            # 把user包装为对象后，包含username,password。TODO: 其他环境8010\8020的转码处理 ？
            # username = user.username
            # password = user.password

            if(module == "Pgm") :
                # 从配置文件读取的内容为unicode编码
                username = user[u"username"]
                real_pwd = (user[u"password"])[unicode(env)]
            else :
                username = user
                real_pwd = user + Env.Env.passwordpostfix
            loginSession = loginERPModule.loginWithEnvDomain(username, real_pwd)
            if loginSession == None:
                RunningLogString.logString = RunningLogString.logString + "登录失败"+ '<br/>'
            else:
                RunningLogString.logString = RunningLogString.logString + "登录成功"+ '<br/>'
        except Exception as ex:
            import logging
            logging.exception("登录失败：")

        # clear path
        sys.path.remove(pathCase)
        return loginSession

    def verifyResult(self):
        if self.responseStatus != 200:
            self.result = "Fail"
        elif self.verifyMode == "code":
            self.modeCodeVerify()
        elif self.verifyMode == "jsonpath":
            self.jsonPathVerify1()
        elif self.verifyMode == "parameter":
            self.jsonPathVerify()
        else:
            self.modeFullMatchVerify()

    def modeCodeVerify(self):
        if str(self.code) == self.expectedResult:
            self.result = "Pass"
        else:
            self.result = "Fail"
        self.actualResult =  self.code

    def modeFullMatchVerify(self):
        # expectedResult is unicode???????
        if str(self.responseContent) == self.expectedResult.encode("utf-8"):
            self.result = "Pass"
        else:
            self.result = "Fail"
        self.actualResult = self.responseContent

    # json
    def jsonPathVerify1(self):
        jsonpath_expr = parse(self.jsonPath)
        match = jsonpath_expr.find(self.responseContent_json)
        if len(match) > 0:
            self.actualResult = match[0].value
        else:
            self.actualResult = ""
        if str(self.actualResult) == str(self.expectedResult):
             self.result = "Pass"
        else:
            self.result = "Fail"

    # json验证的例子
    def jsonPathVerifySamper(self):
        content = self.responseContent
        dictmy = json.loads(content)
        dictmy = {"code":200,"data":{"content":[{
                "code":"108862035747471360",
                "name":"test",
                "year":2015
            },
                                                {
                "code":"108576708885544960",
                "name":"pp",
                "staffVisible":1,
                "stateName":"未启用",
                "year":2015
            }],
        "countable":"999",
        "offset":0,
        "pageNumber":1,
        "pageSize":10,
        "total":786,
        "totalPage":79}}
        pattern = r"/data/content[0]/name"
        path = pattern.strip("/").split("/")
        elem = dictmy
        try:
            for x in path:

                if r"[" in x:
                    indexLeft = x.index("[")
                    indexRight = x.index("]")
                    index1 = x[indexLeft+1:indexRight]
                    key = x[:indexLeft]
                    elem = elem.get(key)[int(index1)]
                else:
                    elem = elem.get(x)
        except:
            pass





















