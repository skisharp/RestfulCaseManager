# -*- coding: utf-8 -*-

import json
import logging
from django.http import HttpResponse
from django.shortcuts import render_to_response
from RestfulCaseManager.Controller.CaseManager import CaseManager
from RestfulCaseManager.Controller.RoleUserMapper import RoleUserMapper
from RestfulCaseManager.Model import Paramter
from RestfulCaseManager.Model import Process
from django import template
from RestfulCaseManager.Model.Env import Env

register = template.Library()

caseManager = CaseManager()

# 跳转到添加测试用例页面
def addcaseHtml(request):
    moduleList = caseManager.getModules()
    roleUserMapper = RoleUserMapper.getRoleUserDict(request.GET.get("module"))
    roles = RoleUserMapper.Roles
    return render_to_response('addcase.html', {"moduleList": moduleList, "roles": roles})

