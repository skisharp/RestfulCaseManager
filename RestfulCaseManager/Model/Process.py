# coding: utf-8

from RestfulCaseManager.util import MongodbOperation
import os
from django.db import models
from django import forms
from mongoengine import *
from RestfulCaseManager.util import JsonExtracter
from RestfulCaseManager.Model import Result
import json
import logging
import Result
import time

'''
class ProcessForm(forms.Form):
     process_name = forms.CharField(label='流程名称', max_length=100)
     process_module = forms.CharField(label='模块', max_length=100)


class Process(models.Model):
    process_name = models.CharField(max_length=100)
    process_module = models.CharField(max_length=3)
'''

'''
# success form
class Process(models.Model):
    process_name = models.CharField(max_length=100)
    process_module = models.CharField(max_length=100)


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['process_name', 'process_module']
'''


class Process(Document):
    connect('assess', host='mongodb://localhost:11111/')
    name = StringField(required=True)
    module = StringField(max_length=50)
    add_time = StringField(max_length=50)


class ProcessOracleCase(Document):
    connection_string = StringField()
    sql = StringField()
    type = StringField()
    process_id = StringField()


class ProcessCase(Document):
    connect('assess', host='mongodb://localhost:11111/')
    name = StringField(required=True)
    url = StringField(required=True)
    data = StringField()
    request_type = StringField(required=True)
    expected_result = StringField()
    verify_mode = StringField()
    verify_expression = StringField()
    role = StringField()
    extractor = StringField()
    module = StringField()
    result = StringField()
    response_status = StringField()
    response_content_json = StringField()
    result_object_id = StringField()
    process_id = StringField()
    order = IntField()
    result_new = ReferenceField(Result.Result)
    call_type = StringField()

    # order by order
    meta = {
        'ordering': ['+order']
    }

    def replace_user_variable(self, user__variable_list, tobe_replace_data):
        import datetime
        replaced_data = tobe_replace_data

        if '$date_year_month_day' in tobe_replace_data:
            now_year_month_day = datetime.datetime.now().strftime('%Y-%m-%d')
            replaced_data = replaced_data.replace('$date_year_month_day', now_year_month_day)

        if '$date_timestamp' in tobe_replace_data:
            now = datetime.datetime.now()
            now_1 = now + datetime.timedelta(days= 2)
            now_1_gmt =  now_1.strftime("%a %b %d %H:%M:%S %Y GMT")
            now_1_timestamp = long(time.mktime(time.strptime(now_1_gmt, "%a %b %d %H:%M:%S %Y %Z")) * 1000)
            replaced_data = replaced_data.replace('$date_timestamp', str(now_1_timestamp))

        if '$date_timestam' in tobe_replace_data:
            now = datetime.datetime.now()
            now_1 = now + datetime.timedelta(days = 3)
            now_1_gmt =  now_1.strftime("%a %b %d %H:%M:%S %Y GMT")
            now_1_timestamp = long(time.mktime(time.strptime(now_1_gmt, "%a %b %d %H:%M:%S %Y %Z")) * 1000)
            replaced_data = replaced_data.replace('$date_timestam', str(now_1_timestamp))

        if '$date_now_two' in tobe_replace_data:
            now = datetime.datetime.now()
            now_1 = now + datetime.timedelta(days= 2)
            now_1_format = now_1.strftime('%Y-%m-%d %H:%M:%S')
            replaced_data = replaced_data.replace('$date_now_two', now_1_format)

        if '$date_now_ten' in tobe_replace_data:
            now = datetime.datetime.now()
            now_1 = now + datetime.timedelta(days= 10)
            now_1_format = now_1.strftime('%Y-%m-%d %H:%M:%S')
            replaced_data = replaced_data.replace('$date_now_ten', now_1_format)

        for k, v in user__variable_list.items():
            if k in tobe_replace_data:
                replaced_data = replaced_data.replace(k, v)

        return replaced_data

    def send_request(self, url, replace_data, params, request_type, rest_quest):
        response = None
        if request_type.lower() == 'get':
            response = rest_quest.restGet(url)
        else:
            if not replace_data:
                replace_data = '{}'
            json_data = json.loads(replace_data)
            if request_type.lower() == 'post':
                response = rest_quest.restPost(url, data=json_data, params=None)
            else:
                response = rest_quest.restPut(url, data=json_data, params=None)
        return response

    def run_oracle_case(self, batch_id):
        import cx_Oracle
        con = cx_Oracle.connect(self.url)
        cur = con.cursor()
        if self.request_type == 'sql_statement':
            cur.execute(self.verify_expression)
            result_list = cur.fetchall()

            str_result = ', '.join(map(str, result_list))
            self.save_result(str_result, 'log', batch_id)
        elif self.request_type == 'proc':
            value = self.verify_expression.encode('utf-8')
            splits = value.split(':')
            package_type = splits[0]
            params = splits[1]
            l = eval(params)
            var_number = cur.var(cx_Oracle.NUMBER)
            var_string = cur.var(cx_Oracle.STRING)
            cur.callproc(package_type, (l[0], l[1], l[2], var_string, var_number))
            print var_number.getvalue()
            self.save_result(var_number.getvalue(), 'log', batch_id)
        else:
            value = self.verify_expression.encode('utf-8')
            splits = value.split(':')
            package_type = splits[0]
            params = splits[1]
            l = eval(params)
            var_number = cur.var(cx_Oracle.NUMBER)
            var_string = cur.var(cx_Oracle.STRING)
            var_number = cur.var(cx_Oracle.NUMBER)
            self.save_result(var_string.getvalue(), 'log', batch_id)
        cur.close()
        con.close()
        return {"flag": True, "batch_id": batch_id}

    # 运行 主函数
    def run_case(self, module, env, user_variable_list, batch_id):
        # 表示case运行状态 False 是失败

        if self.call_type == 'Oracle':
            self.run_oracle_case(batch_id)

        flag = True

        log_string = '==========开始运行测试用例：' + self.name + '</br>'

        context = self.set_up_case(module=module, env=env)
        if context is None:
            flag = False
            return flag

        log_string += '1： 获取环境变量成功<br/>'

        # 替换用户定义的参数
        replace_data = self.replace_user_variable(user_variable_list, self.data)
        replace_url = self.replace_user_variable(user_variable_list, self.url)
        log_string += '2： 替换用户定义的参数成功<br/>'

        # 登录
        from RestfulCaseManager.Case import loginERP
        session = loginERP.login(context.login_domain, self.role, self.role + context.password_postfix)
        if session is None:
            flag = False
            return flag
        string_temp = '3：  用户：' + self.role + '<br/>密码：'+ self.role + context.password_postfix + ':登录成功<br/>'
        log_string += string_temp

        # 发送请求
        from RestfulCaseManager.Controller import RestRequest

        rest_quest = RestRequest.RestRequest(session)
        url = context.domain + replace_url

        if self.data.startswith('{') or self.data.encode('utf-8') == '':
            response = self.send_request(
                url=url,
                replace_data=replace_data,
                params=None,
                request_type=self.request_type,
                rest_quest=rest_quest)
        else:
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
            session.headers = headers
            response = session.post(url=url, data=replace_data)

        loginERP.logout(context.login_domain)

        string_temp = '4：  开始发送请求<br/>'
        string_temp += "URL：" + url + '<br/>'
        string_temp += "请求方法：" + self.request_type.encode('utf-8') + '<br/>'
        string_temp += "数据：" + replace_data.encode('utf-8') + '<br/>'

        string_temp += '5： 返回结果<br/>'
        string_temp += "响应码：" + str(response.status_code).encode('utf-8') + '<br/>'
        string_temp += "响应内容：<br/>"
        string_temp += response.content + '<br/>'
        log_string += string_temp

        if response is None:
            flag = False
            return flag

        # 提取用户自定义参数
        if self.extractor:
            self.extract_params(json.loads(response.content), self.extractor, user_variable_list)
        log_string += '6： 提取用户自定义参数<br/>'
        log_string += json.dumps(user_variable_list)

        # 保存运行结果
        result_final = self.save_result(response, log_string, batch_id)

        return result_final

    def save_result(self, response, log_string, batch_id):
        if self.call_type == 'Oracle':
            result = Result.Result(
            case_id=self.id,
            result='Fail',
            actual_result=str(response),
            batch_id=batch_id,
            running_log=log_string
            )
            result.save()
            self.result_new = result
            self.save()

            return {"flag": True, "batch_id": batch_id}

        flag = True

        response_status = response.status_code
        response_content = response.content

        result = None
        # 如果请求返回不是200， 则失败返回
        if response_status != 200:
            result = Result.Result(
                case_id=self.id,
                result='Fail',
                actual_result='',
                response_status=str(response_status),
                response_content=response_content,
                batch_id=batch_id,
                running_log=log_string
            )
            flag = False

        else:
            response_content_json = None
            if response_content != "":
                try:
                    response_content_json = json.loads(response_content)
                except:
                    logging.exception("responseContent_json")

            # 结果
            if self.verify_expression:
                actual_result = JsonExtracter.JsonExtractor.extract_value(response_content_json, self.verify_expression)
            else:
                actual_result = ''

            if str(actual_result) == self.expected_result:
                result_string = 'Pass'
            else:
                result_string = 'Fail'
                flag = False

            result = Result.Result(
                case_id=self.id,
                result=result_string,
                actual_result=str(actual_result),
                response_status=str(response_status),
                response_content=response_content,
                batch_id=batch_id,
                running_log=log_string
            )

        result.save()
        self.result_new = result
        self.save()

        return {"flag": flag, "batch_id": batch_id}

    def extract_params(self, response_content_json,  extractor, user_variable_list):
        if extractor != '':
            variable_list = extractor.split(':')
            for item in variable_list:
                splits = item.split(',')
                try:
                    value = JsonExtracter.JsonExtractor.extract_value(response_content_json, splits[2])
                    user_variable_list[splits[0]] = value
                except:
                    import logging
                    logging.exception("提取参数失败！")


    def set_up_case(self, module, env):
        from RestfulCaseManager.Model import Context
        from RestfulCaseManager.util import ConfigReader
        context = Context.Context()
        config_parser = ConfigReader.read_conf(module=module)
        context.domain = config_parser.get(env, "domain")
        context.login_domain = config_parser.get(env, "logindomain")
        context.password_postfix = config_parser.get(env, "passwordpostfix")
        return context

    def tear_down_case(self):
        print 'tear_down'


class ProcessRunner():
    def __init__(self):
        pass

    def run_process(self, process_id, env, batch_id):
        user_variable_list = {}
        case_list = ProcessCase.objects(process_id=str(process_id))

        process_item = Process.objects.get(id=process_id)
        result_final = None
        for case in case_list:
            result_final = case.run_case(module=process_item.module,
                                         env=env,
                                         user_variable_list=user_variable_list,
                                         batch_id=batch_id)

        return result_final




















