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

# 链接到添加参数页
def addParamterHtml(request):
    return render_to_response('add_paramter.html')

# 添加参数到DB
def addParameerToDB(request):
    paramter = Paramter.Paramter(request.POST.get('name'),request.POST.get('value'),request.POST.get('method'),request.POST.get('module'))
    paramter.addParamter()
    return HttpResponse("<script language=javascript>alert('success');url ='http://'+window.location.host + '/paramters_list/'; window.location.href=url;</script>")
