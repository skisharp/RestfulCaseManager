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


# 跳转到历史结果页面
def historyResultHtml(request):
    caseId = request.GET.get("caseId")
    resultList = caseManager.getHistoryResult(caseId)
    case = caseManager.getCaseById(caseId)
    return render_to_response('history_result.html', {"resultList": resultList, "case": case})

# 查看运行log
def caseLog(request):
    from RestfulCaseManager.Model import Result
    logging = None

    if 'case_id' in request.GET:
        logging = Result.Result.objects.get(case_id=request.GET.get('case_id'), batch_id=request.GET.get('batch_id')).running_log
    else:
        resultId = request.GET["resultId"]
        logging = caseManager.get_result_logging(resultId)
    return render_to_response('caselog.html', {'logging': logging})


def testajax(request):
    return render_to_response('testajax.html')


def returnjson(request):
    ret = {{'aaaa': 'ooooo', 'nnnn': "ooooo"},'count',20}
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)


def zrx(request):
    print '================'
    print request
    print dir(request)
    print request.get_host()
    from RestfulCaseManager.Model import Module
    module_list = Module.Module.objects

    print len(module_list)
    for item in module_list:
        print item.name
    return render_to_response('testbootstramp.html')


def index(request):
    from django import forms
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Your name', max_length=100)
        your_name1 = forms.CharField(label='Your 333', max_length=100)
        your_name2 = forms.CharField(label='Your 222', max_length=100)
        sender = forms.EmailField()
        cc_myself = forms.BooleanField(required=False)
        cc_myself1 = forms.URLField(required=False)
        abc = forms.ComboField()
        aaa = forms.CheckboxInput()
    return render_to_response('testajax.html', {"form" : NameForm()})

DEBUG_TOOLBAR_CONFIG = {
'SHOW_TOOLBAR_CALLBACK': list
}

