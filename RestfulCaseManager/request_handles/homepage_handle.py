# -*- coding: utf-8 -*-
import logging

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import template
from mongoengine.errors import DoesNotExist
from RestfulCaseManager.Controller.CaseManager import CaseManager
from RestfulCaseManager.Controller.HistoryManager import HistoryManager
from RestfulCaseManager.Model import Paramter
from RestfulCaseManager.Model import Process
from RestfulCaseManager.Model import Module


register = template.Library()
caseManager = CaseManager()
historyManager = HistoryManager()



# home page
def homepage(request):
    module_list = Module.Module.objects
    module_count = len(module_list)

    line = module_count / 4
    final_line_count = module_count % 4

    return render_to_response('index.html',
                              {"module_list": module_list,
                               "line": line,
                               "final_line_count": final_line_count,
                               'loop_times': range(1, 6)
                               })


# 链接到添加模块页面
def add_module_html(request):
    return render_to_response('add_module.html')


# add and save to db
def save_module_db(request):
    name = request.POST.get("name")
    owner = request.POST.get("owner")

    module = Module.Module(name=name, owner=owner)
    module.save()
    module.init_module()

    return HttpResponse("<script language=javascript>alert('success');"
                        "url ='http://'+window.location.host + '/index/'; "
                        "window.location.href=url;</script>")


# 链接到参数列表页
def paramtersListHtml(request):
    paramter = Paramter.Paramter()
    getDict = request.GET
    if "module" in getDict.keys():
        parameterList = paramter.getParameters(request.GET.get("module"))
    else:
        parameterList = paramter.getParameters("test")
    return render_to_response('paramters_list.html', {'caseList': parameterList})


# 跳转到管理测试用例
def manageCase(request):
    getDict = request.GET

    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
        rowNum = int(request.GET.get('rowNum', 10))


    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
        searchText = ''

    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    start_pos = (curPage - 1) * rowNum

    caseCount = 0
    # 根据该模块的case
    if "searchText" not in getDict.keys():
        if "module" in getDict.keys():
            if "order" in getDict.keys():
                caseList = caseManager.getCaseList(request.GET.get("module"), request.GET.get("order"),request.GET.get('rowNum'))
            else:
                #这里的caseList是cursor
                caseList = caseManager.getCaseList(module=request.GET.get("module"), start_index=start_pos, row_num=rowNum)
                #之前用的deepcopy方法
                #import copy
                #caseListCopy = caseList.__deepcopy__(caseList)
        else:
            caseList = caseManager.getCaseList()
    else:
        print "homepage_handle"+request.GET.get("module")+request.GET.get('searchText')
        caseList = caseManager.getSearchCaseList(module=request.GET.get("module"), start_index=start_pos, text=request.GET.get('searchText'))
        rowNum=100

    case_list = list(caseList) # change cursor to list
    caseIdList = caseManager.getCaseIdList(iter(case_list))
    latestRunResultList = caseManager.findLatestRunResultListByCaseIdList(caseIdList = caseIdList)
    caseManager.getRealList(case_list,latestRunResultList)



    if caseList:
        caseCount = caseList.count()

    allPage = caseCount / rowNum
    remainPost = caseCount % rowNum
    if remainPost > 0:
        allPage += 1

    # 'latestRunResultList':latestRunResultList,
    # 'latestRespnseList':latestRespnseList,

    return render_to_response('managecase.html',
                              {'caseList': case_list,
                               'latestRunResultList': latestRunResultList,
                               "caseCount": caseCount,
                               'curPage': curPage,
                               'allPage': allPage,
                               'rowNum': rowNum,
                               "module": request.GET.get("module")})


def process_flow_html(request):

    module = request.GET.get('module')
    try:
        process_list = Process.Process.objects(module=module)
    except DoesNotExist:
        logging.exception("没有查到任何记录！")
    except:
        logging.exception("加载流程失败")

    process_count = process_list.count()

    return render_to_response('process_list.html',
                                {
                                    "process_list": process_list,
                                    "process_count": process_count,
                                    "module": request.GET.get("module")
                                }
                            )