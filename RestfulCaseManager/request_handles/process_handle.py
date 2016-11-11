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
from RestfulCaseManager.Model import Process
from django.forms import forms
from django.forms import ModelForm
from mongoengine import *
from RestfulCaseManager.Model import Process
from RestfulCaseManager.Model import Result

caseManager = CaseManager()


# 跳转到添加流程页面
def add_process_html(request):
    # form = process.ProcessForm()
    # return render_to_response('add_process.html', {"form": form})
    # type: add, edit
    type = request.GET.get('type')
    if type == 'add':
        module = request.GET.get('module')
        return render_to_response('add_process.html', {"module": module, "type": type})
    else:
        process_item = Process.Process.objects.get(id=request.GET.get('process_id'))
        return render_to_response('add_process.html', {"process_item": process_item, "type": type})


# 跳转到添加 数据库操作case
def add_oracle_case_html(request):
    process_id = request.GET.get('process_id')
    type_list = ['sql_statement', 'func', 'proc']
    return render_to_response('add_oracle_case.html',
                              {"process_id": process_id,
                               "type_list": type_list})


def save_oracle_case(request):
    case_id = request.POST.get('case_id')
    print case_id
    sql_case = Process.ProcessCase()
    if case_id != '':
        sql_case = Process.ProcessCase.objects.get(id=case_id)
    process_id = request.POST.get('process_id')
    name = request.POST.get('name')
    connection_string = request.POST.get('connection_string')

    sql_case.process_id = process_id
    sql_case.name = name
    sql_case.call_type = 'Oracle'
    sql_case.request_type = request.POST.get('type')
    sql_case.url = connection_string
    sql_case.verify_expression = request.POST.get('call_value')
    sql_case.expected_result = request.POST.get('expected_result')

    sql_case.save()
    return HttpResponse("<script language=javascript>alert('save success!');url ='http://'+window.location.host + '/process_case_list?process_id="  + process_id +"'; window.location.href=url;</script>")

# 添加流程到数据库
def add_process_to_db(request):
    name = request.POST.get('name').encode('utf-8')
    module = request.POST.get('module').encode('utf-8')
    process_id = request.POST.get('process_id')
    import datetime
    now = datetime.datetime.now()
    add_time = now.strftime('%c')
    if process_id:
        process_new = Process.Process.objects.get(id=process_id)
        process_new.name = name
        process_new.module = module
        process_new.save()
        return HttpResponse("<script language=javascript>alert('edit success');url ='http://'+window.location.host + '/processflowhtml?module="+module+"'; window.location.href=url;</script>")
    else:
        process_new = Process.Process(name=name, module=module, add_time=add_time)
        process_new.save()
        return HttpResponse("<script language=javascript>alert('add success');url ='http://'+window.location.host + '/processflowhtml?module="+module+"'; window.location.href=url;</script>")


def delete_process(request):
    process_id = request.GET.get('process_id').encode('utf-8')
    process_item = Process.Process.objects.get(id=process_id)
    process_item.delete()
    return HttpResponse("<script language=javascript>alert('delete success');url ='http://'+window.location.host + '/processflowhtml?module="+process_item.module+"'; window.location.href=url;</script>")


def process_case_list(request):
    process_id = request.GET.get('process_id')
    process_item = Process.Process.objects.get(id=process_id)
    process_case_list = Process.ProcessCase.objects(process_id=process_id)
    process_case_list_count = process_case_list.count()

    return render_to_response('process_case_list.html',
                              {"process_case_list": process_case_list,
                               "process_case_list_count": process_case_list_count,
                               "process_item": process_item
                              })


# 跳转到添加流程case页面
def add_process_case_html(request):
    process_id = request.GET.get('process_id')
    process_item = Process.Process.objects.get(id=process_id)
    case = None
    return render_to_response('add_process_case.html', {'case': case, "process_item": process_item })


# 保存process case
def save_process_case(request):
    process_id = request.POST.get('process_id')
    case_id = request.POST.get('case_id')

    if case_id:
        save_case(request, 'edit')
    else:
        save_case(request, 'add')

    return HttpResponse("<script language=javascript>alert('save success!');url ='http://'+window.location.host + '/process_case_list?process_id="  + process_id +"'; window.location.href=url;</script>")


def save_case(request, operator):
    process_id = request.POST.get('process_id')
    name = request.POST.get('name').encode('utf-8')
    url = request.POST.get('url').encode('utf-8')
    data = request.POST.get('data').encode('utf-8')
    request_type = request.POST.get('request_type').encode('utf-8')
    expected_result = request.POST.get('expected_result').encode('utf-8')
    verify_mode = request.POST.get('verify_mode').encode('utf-8')
    verify_expression = request.POST.get('verify_expression').encode('utf-8')
    role = request.POST.get('role').encode('utf-8')
    extractor = request.POST.get('extractor').encode('utf-8')

    if operator == 'add':
        process_case = Process.ProcessCase(name=name,
                                           url=url,
                                           data=data,
                                           request_type=request_type,
                                           expected_result=expected_result,
                                           verify_mode=verify_mode,
                                           verify_expression=verify_expression,
                                           role=role,
                                           extractor=extractor,
                                           process_id=process_id)

    else:
        process_case = Process.ProcessCase.objects.get(id=request.POST.get('case_id').encode('utf-8'))
        process_case.name = name
        process_case.url = url
        process_case.data = data
        process_case.request_type = request_type
        process_case.expected_result = expected_result
        process_case.verify_mode = verify_mode
        process_case.verify_expression = verify_expression
        process_case.role = role
        process_case.extractor = extractor

    process_case.save()


# 删除case
def delete_process_case(request):
    case_id = request.GET.get('case_id')
    case = Process.ProcessCase.objects.get(id=case_id)
    process_id = case.process_id
    case.delete()

    return HttpResponse("<script language=javascript>alert('delete success!');url ='http://'+window.location.host + '/process_case_list?process_id="  + process_id +"'; window.location.href=url;</script>")


# 复制case
def copy_process_case(request):
    case_id = request.GET.get('case_id')
    case = Process.ProcessCase.objects.get(id=case_id)
    case_clone = Process.ProcessCase(name=case.name,
                                    url=case.url,
                                    data=case.data,
                                    request_type=case.request_type,
                                    expected_result=case.expected_result,
                                    verify_mode=case.verify_mode,
                                    verify_expression=case.verify_expression,
                                    role=case.role,
                                    extractor=case.extractor,
                                    process_id=case.process_id,
                                    )
    case_clone.save()
    process_id = case.process_id
    return HttpResponse("<script language=javascript>alert('copy success!');url ='http://'+window.location.host + '/process_case_list?process_id="  + process_id +"'; window.location.href=url;</script>")


# 跳转到 编辑case页面
def edit_process_case(request):
    case_id = request.GET.get('case_id')
    case = Process.ProcessCase.objects.get(id=case_id)
    request_type_list = ['put', 'get', 'post']
    return render_to_response('add_process_case.html', {'case': case, "request_type_list": request_type_list})


# 保存case顺序
def save_order(request):
    import json
    if request.method == 'POST':
        abc = request.POST.items()[0][0].encode('utf-8')
        d = json.loads(abc)
        for key in d:
            case = Process.ProcessCase.objects.get(id=key)
            case.order = int(d[key])
            try:
                case.save()
            except:
                logging.exception("case 保存顺序失败！")

    message_return_json = json.dumps({"message": "successful"})
    return HttpResponse(message_return_json, content_type='application/json')


# 运行流程
def run_process_case(request):
    process_id = request.GET.get('process_id')
    env = request.GET.get('env')

    Result.Result.objects().delete()

    runner = Process.ProcessRunner()
    from bson.objectid import ObjectId
    batch_id = ObjectId()
    result_final = runner.run_process(process_id, env, batch_id)
    message_return_json = None
    request_host = request.get_host()
    show_result_url = 'http://' + request_host + '/show_result?process_id=' + process_id + '&status='
    if result_final['flag']:
        show_result_url += 'success&batch_id='
        show_result_url += str(result_final.get('batch_id'))
        message_return_json = json.dumps({"message": "success",
                                          "batch_id": str(result_final.get('batch_id')),
                                          "result_url": show_result_url})
    else:
        message_return_json = json.dumps({"message": "fail",
                                          "batch_id": str(result_final.get('batch_id')),
                                          "result_url": show_result_url})

    return HttpResponse(message_return_json, content_type='application/json')


def show_result(request):
    process_id = request.GET.get('process_id')
    batch_id = request.GET.get('batch_id')
    process_item = Process.Process.objects.get(id=process_id)
    case_list = Process.ProcessCase.objects(process_id=process_id)

    running_status = 'Pass'
    for item in case_list:
        if item.result_new.result == 'Fail':
            running_status = 'Fail'

    return render_to_response("process_case_result.html",
                              {"process_item": process_item,
                               "batch_id": batch_id,
                               'case_list': case_list,
                               'running_status': running_status})


def show_module_process_result(request):
    module = request.GET.get('module')
    batch_id = request.GET.get('batch_id')
    result = Result.Result.objects(batch_id=batch_id)
    process_list = Process.Process.objects(module=module)

    context1 = {}
    context1['message'] = 'success'

    context1_data = []
    fail_count = 0

    for process in process_list:
        flag = True
        process_data = {}
        process_data['name'] = process.name
        case_list = Process.ProcessCase.objects(process_id=str(process.id))
        case_list2 = []
        for case in case_list:
            result = Result.Result.objects.get(batch_id=str(batch_id), case_id=case.id)
            result_data = {
                "batch_id": batch_id,
                "case_id": case.id,
                "case_name": case.name,
                "result": result.result,
                "actual_result": result.actual_result,
                "expected_result": case.expected_result,
                "response_status": result.response_status,
                "response_content": result.response_content}
            if result.result == 'Fail':
                flag = False
            case_list2.append(result_data)
        process_data['caselist'] = case_list2
        context1_data.append(process_data)
        if not flag:
            fail_count += 1
    context1['data'] = context1_data
    context1['fail_count'] = fail_count
    context1['process_count'] = len(process_list)

    return render_to_response("module_process_case_result.html", context1)


def run_module_process(request):
    module = request.GET.get('module')
    env = request.GET.get('env')
    process_list = Process.Process.objects(module=module)
    runner = Process.ProcessRunner()
    #
    result_final = None
    from bson.objectid import ObjectId
    batch_id = ObjectId()
    for item in process_list:
        result_final = runner.run_process(item.id, env, batch_id)
    request_host = request.get_host()
    show_result_url = 'http://' + request_host + '/show_module_process_result?module=' + module + '&batch_id=' + str(batch_id)
    message_return_json = json.dumps({"message": "success",
                                          "batch_id": str(batch_id),
                                          "result_url": show_result_url})
    return HttpResponse(message_return_json, content_type='application/json')


def edit_oracle_case(request):
    case_id = request.GET.get('case_id')
    case = Process.ProcessCase.objects.get(id=case_id)
    type_list = ['sql_statement', 'func', 'proc']
    return render_to_response('edit_oracle_case.html',
                              {"case": case,
                               "type_list": type_list})


def copy_process(request):
    process_id = request.GET.get('process_id')
    process = Process.Process.objects.get(id=process_id)
    case_list = Process.ProcessCase.objects(process_id=process_id)
    import datetime
    now = datetime.datetime.now()
    add_time = now.strftime('%c')

    process_clone = Process.Process(name=process.name,
                                    module=process.module,
                                    add_time=add_time
                                    )
    process_clone.save()
    for case in case_list:
        case_clone = clone_process_case(case.id)
        case_clone.process_id = str(process_clone.id)
        case_clone.save()

    return HttpResponse("<script language=javascript>alert('copy success');url ='http://'+window.location.host + '/processflowhtml?module="+process_clone.module+"'; window.location.href=url;</script>")


def clone_process_case(case_id):
    case = Process.ProcessCase.objects.get(id=case_id)
    case_clone = Process.ProcessCase(name=case.name,
                                    url=case.url,
                                    data=case.data,
                                    request_type=case.request_type,
                                    expected_result=case.expected_result,
                                    verify_mode=case.verify_mode,
                                    verify_expression=case.verify_expression,
                                    role=case.role,
                                    extractor=case.extractor,
                                    process_id=case.process_id,
                                    )
    case_clone.save()
    return case_clone



