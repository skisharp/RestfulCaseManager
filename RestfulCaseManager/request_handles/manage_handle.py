# -*- coding: utf-8 -*-
import json
import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import template

from RestfulCaseManager.Controller.CaseManager import CaseManager

from RestfulCaseManager.Controller.RoleUserMapper import RoleUserMapper
from RestfulCaseManager.Model.Env import Env

register = template.Library()
caseManager = CaseManager()


# 跳转到添加测试用例页面
def add_case_html(request):
    module_list = caseManager.getModules()


    module_default = request.GET.get('module')


    roleUserMapper = RoleUserMapper.getRoleUserDict(request.GET.get("module"))
    roles = RoleUserMapper.Roles
    return render_to_response('addcase.html',
                              {"module_list": module_list,
                               "module_default": module_default,
                               "roles": roles})

#管理测试角色用户名密码 以列表的方式进行 右上角有添加角色用户密码
def role_user_list(request):

    role_list ={
        "module": "Mtool",
        "role": "Manager",
        "username": "jingwang",
        "pwd": "jingwangpgmtest644",
        "env": "8030",
    }

    return render_to_response('role_user_list.html',{"role_list":role_list})

#添加测试角色用户名密码
def add_role_user_html(request):

    return render_to_response('add_role_user.html')



# 添加测试用例到DB
def addCase(request):
    name = request.POST.get('name').encode('utf-8')
    if name == "":
        return HttpResponse("Name should not be empty!")
    url = request.POST.get('url')
    if url == "":
        return HttpResponse("url should not be empty!")
    requestType = request.POST.get('requestType').encode('utf-8')
    if requestType == "":
        return HttpResponse("requestType should not be empty!")

    # 判断是否有重复的name
    for case in caseManager.getCaseList():
        if "name" in case.keys():
            if case["name"] == name:
                return HttpResponse("<script language=javascript>alert('Name is dup!');url ='http://'+window.location.host + '/homepage/'; window.location.href=url;</script>")

    module = request.POST.get('module').encode('utf-8')
    data = request.POST.get('data').encode('utf-8')

    expectedResult = request.POST.get('expectedResult').encode('utf-8')
    verifyMode = request.POST.get('verifyMode').encode('utf-8')
    comment = request.POST.get('comment').encode('utf-8')
    priority = request.POST.get('priority').encode('utf-8')
    jsonPath = request.POST.get('path').encode('utf-8')
    role = request.POST.get('role').encode('utf-8')
    import datetime
    now = datetime.datetime.now()
    nowString = now.strftime('%c')

    postData = {
            "name": name,
            "module" : module,
            "url" : url,
            "requestType" : requestType,
            "data" : data,
            "expectedResult" : expectedResult,
            "verifyMode" : verifyMode,
            "priority" : priority,
            "jsonPath": jsonPath,
            "role": role,
            "addTime":nowString,
            "comment": comment
        }

    # add case
    caseManager.addCase(postData)

    return HttpResponse("<script language=javascript>alert('添加测试用例成功!');url ='http://'+window.location.host + '/manage?module="  + module +"'; window.location.href=url;</script>")


# 导出case
def exportCaseTofile(request):
    caseManager.exportCasesToFile333()
    return HttpResponse("success")

#  执行case
def runCase(request):
    getDict = request.GET
    module = request.GET.get("module")
    env = request.GET.get("env")
    caseId = request.GET.get("caseId")
    # 设定环境信息
    Env.setting(module=module, env=env)
    # 获取角色和用户的mapper
    RoleUserMapper.getRoleUserDict(module=module)
    if "caseId" in getDict.keys():
        result_final = caseManager.runCase(caseId=caseId, env=env, module=module)
    elif "module" in getDict.keys():
        result_final = caseManager.runCase(module=module, env=env)
    else:
        result_final = caseManager.runCase("test", "8030")
    request_host = request.get_host()
    show_result_url = 'http://' + request_host +'/show_case_result?batch_id='
    show_result_url += str(result_final.get('batch_id'))
    message_return_json = json.dumps({"message": "success",
                                          "batch_id": str(result_final.get('batch_id')),
                                          "result_url": show_result_url})

    return HttpResponse(message_return_json, content_type='application/json')


def show_case_result(request):
    param_dict = request.GET
    batch_id = param_dict.get('batch_id')
    result_list = caseManager.get_result(batch_id=batch_id)
    count_all = result_list.count()
    success_count = 0
    list_all = []
    for item in result_list:
        case_temp = caseManager.getCaseById(item['caseId'])
        list_all.append({"caseName": item['caseName'],
                         "result": item['result'],
                         "responseCode": item['responseCode'],
                         "actualResult": item['actualResult'],
                         "response": item['response'],
                         "resultObjectId": item['_id'],
                         "caseId": item['caseId'],
                         "expectedResult": case_temp['expectedResult'],
                         "runningTime": item['runningTime']})
        if item['result'] == 'Pass':
            success_count += 1

    fail_count = count_all - success_count

    return render_to_response('result.html',
                              {'result_list': list_all,
                               "count": count_all,
                               'success_count': success_count,
                               'fail_count': fail_count})


# 上传case文件
# def uploadFile(request):
#     caseFile = request.FILES['caseFile']
#     aaa = ''
#     for chunk in caseFile.chunks():
#         aaa = aaa + chunk
#
#     with open("name.json", "wb+") as test2222:
#         # test2222.write(aaa.decode('gbk').encode('utf8'))
#         test2222.write(aaa)
#
#     logging.info("========================上传到name.txt文件成功")
#
#     try:
#         file = open("name.json", 'r')
#     except:
#         logging.exception("上传文件打开失败")
#
#     # case_json = json.loads(aaa.decode('gbk').encode('utf8'))
#     case_json = json.loads("{}")
#     try:
#         case_json = json.loads(aaa)
#     except:
#         logging.exception("load json 文件失败：")
#         return HttpResponse("<script language=javascript>alert('上传文件格式错误，请重新上传!');url ='http://'+window.location.host + '/manage/'; window.location.href=url;</script>")
#     # case_json = json.load(file)
#     dataTemp = ''
#     moduleTemp = ''
#     commentTemp = ''
#     priorityTemp = ''
#
#     for case in case_json["testcases"]:
#
#         if case["RequestMethod"] == 'Get':
#             dataTemp = {}
#         else:
#             dataTemp = case["data"]
#         if case.has_key("Module"):
#             moduleTemp = case["Module"]
#         if case.has_key('Comment'):
#             commentTemp = case["Comment"]
#         if case.has_key('Priority'):
#             priorityTemp = case["Priority"]
#
#         # json.dumps 可以去掉dict中的u
#         postData = {
#                 "name": case["name"],
#                 "module": moduleTemp,
#                 "url": case["url"],
#                 "requestType" : case["RequestMethod"],
#                 "data": json.dumps(dataTemp),
#                 "expectedResult": case["ExpectedResult"],
#                 "verifyMode": case["VerifyMode"],
#                 "priority": priorityTemp,
#                 "comment": commentTemp,
#                 "jsonPath": case["JsonPath"]
#         }
#         # case_json = json.load(destination,encoding='utf-8')
#         caseManager = CaseManager()
#         caseManager.addCase(postData)
#
#     return HttpResponse("<script language=javascript>alert('success!');url ='http://'+window.location.host + '/manage?module="  + moduleTemp +"'; window.location.href=url;</script>")

# 删除测试用例
def deletecase(request):
    caseId = request.GET['caseId'].encode('utf-8')
    module = request.GET['module'].encode('utf-8')
    caseManager.delete_case(caseId)
    return HttpResponse("<script language=javascript> alert('delete success!'); url ='http://'+window.location.host + '/manage?module=" + module + "'; window.location.href=url;</script>")

# 跳转到copy一个测试用例
def copyCase(request):
    caseId = request.GET["caseId"].encode('utf-8')
    case = caseManager.getCaseById(caseId)
    moduleList = caseManager.getModules()
    priorityList = caseManager.getPriorityList()
    verifyModeList = caseManager.getVerifyModeList()
    requestTypeList = caseManager.getRequestTypeList()
    roles = RoleUserMapper.getRoleUserDict(case["module"])
    return render_to_response('copy.html', {'case': case, 'moduleList':moduleList,'priorityList':priorityList,'verifyModeList':verifyModeList,'requestTypeList':requestTypeList,'roles':roles})

# 跳转到修改测试用例页面
def modifyCase(request):
    caseId = request.GET["caseId"].encode('utf-8')
    case = caseManager.getCaseById(caseId)
    verifyModeList = ["jsonpath",'code','fullmatch','regex']
    RoleUserMapper.getRoleUserDict(case['module'])
    roles = RoleUserMapper.Roles
    return render_to_response('modify.html', {'case': case, 'verifyModeList': verifyModeList,'roles':roles})


# 修改测试用例页面
def updateCase(request):
    request.encoding = 'utf-8'
    caseId = request.POST.get('caseId')
    # case 名字
    name = request.POST.get('name').encode('utf-8')
    if name == "":
        return HttpResponse("Name should not be empty!")
    # case url
    url = request.POST.get('url').encode('utf-8')
    if url == "":
        return HttpResponse("url should not be empty!")
    # case request 方法
    requestType = request.POST.get('requestType')
    if requestType == "":
        return HttpResponse("requestType should not be empty!")
    else:
        name = request.POST.get('name')
        module = request.POST.get('module')
        data = request.POST.get('data')
        expectedResult = request.POST.get('expectedResult')
        verifyMode = request.POST.get('verifyMode')
        priority = request.POST.get('priority')
        jsonPath = request.POST.get('path')
        role = request.POST.get('role')
        comment = request.POST.get('comment')

        now = datetime.datetime.now()
        now_string = now.strftime('%c')

        post_data = {
            "name": name,
            "module": module,
            "url": url,
            "requestType": requestType,
            "data": data,
            "expectedResult": expectedResult,
            "verifyMode": verifyMode,
            "priority": priority,
            "addTime": now_string,
            "jsonPath": jsonPath,
            "role": role,
            "comment": comment,
            }

        # update case
        caseManager.updateCase(caseId, post_data)

        return HttpResponse("<script language=javascript>alert('update success!');url ='http://'+window.location.host + '/manage?module="  + module +"'; window.location.href=url;</script>")







