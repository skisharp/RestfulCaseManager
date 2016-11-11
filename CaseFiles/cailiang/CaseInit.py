# coding:UTF-8
# from ConfigParser import ConfigReader
import json
from RestfulCaseManager.util import ConfigReader
import loginERP
from RestfulCaseManager.Controller.RestRequest import RestRequest
import logging


class CaseInitBase(object):
    def initCase(self):
        pass

class Mtool(object):
    def test(self):
        print 'testtesttesttest!!!!!!!!!!!!!!!'


class CaseInit(CaseInitBase):
    def initCase(self,module, env):
        print '======Mtool.json case init!'
        self.setInitInfo(module, env)
        self.loginERP()
        self.addALiuWeiData()
        logging.info(module)
        logging.info("初始化成功！")
        return self.restRequest

    # 还可以再初始化中加入参数 params
    def addALiuWeiData(self):
        # 增加一个新的六维评价
        data = {"empId":"378030","entryType":"MANAGER","dimensionId":"","dimensionDate":"2016-01-23","keyPosition":{"sixDemiValue":"N","comment":"","readynow":"","oneyear":"","twoyear":""},"personState":{"sixDemiValue":"H","mainCode":"","detailCode":"","comment":""},"positionAttract":{"sixDemiValue":"H","mainCode":"","detailCode":"","comment":""},"dutyState":{"sixDemiValue":"H","mainCode":"","detailCode":"","comment":""},"resignRisk":{"sixDemiValue":"L","resRiskSixMonth":"","resRiskOneYear":"","resRiskTwoYear":"","resRiskDeal":"","comment":""}}
        url_temp = self.domain + '/apex-s/mt/mtmain/saveSixDimen'
        response = self.restRequest.restPost(url_temp,data=data,params=None)
        # responseContent_json = json.loads(response.content)
        # dimenId = responseContent_json['data']['dimenId']

    # 登录erp
    def loginERP(self):
        self.loginSession = loginERP.login(self.loginDomain,self.user,self.user + self.passwordpostfix)
        self.restRequest = RestRequest(self.loginSession)

    # 从conf中读取用户信息
    def setInitInfo(self,module, env):
        self.conf = ConfigReader.read_conf(module)
        self.domain = self.conf.get(env, "domain")
        self.user = self.conf.get(env, "user")
        self.loginDomain = self.conf.get(env, "logindomain")
        self.passwordpostfix = self.conf.get(env, "passwordpostfix")