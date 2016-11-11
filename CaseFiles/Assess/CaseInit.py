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


class CaseInit(CaseInitBase):
    def initCase(self,module, env):
        print '======Assess.json case init!'

