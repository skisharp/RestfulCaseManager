# coding: UTF-8

import requests
import re
import json
import sys
import logging
from  RestfulCaseManager.Model import Env

def loginWithEnvDomain(username, password):
    return login(loginDomain=Env.Env.logindomain, username=username,password=password)


def login(loginDomain, username, password):
    session = requests.Session()
    url = loginDomain

    # first step
    r = session.get(url)
    # get lt
    lt = getlt(r.content)

    # second step
    user_data = {'username': username,
                 'password': password,
                 'rememberMe':'on',
                 'execution':'e1s1',
                 '_eventId':'submit',
                 'type':'1',
                 'lt': lt
    }
    r = session.post(url, data=user_data)

    # third step login success
    user_data = {
                        "execution": "e1s2",
                        "_eventId": "submit"
    }
    r = session.post(url, data=user_data)
    print '==========================='
    print r.content


    url_assess_answer = Env.Env.login_domain_answer
    user_data = {'username': username,
                 'password': password,
                 'rememberMe':'on',
                 'execution':'e1s1',
                 '_eventId':'submit',
                 'type':'1',
                 'lt': lt
    }
    r = session.post(url_assess_answer, data=user_data)

    user_data = {
                    "execution": "e1s2",
                    "_eventId": "submit"
    }
    r = session.post(url_assess_answer, data=user_data)

    return session


def login22(loginDomain, username, password):
    # session = None
    try:
        logging.info("=======" + username + "=======开始登录")
        logging.info("=======" + password + "=======密码")
        session = requests.Session()
        # url = domain + "/login?service=http%3A%2F%2Ferp8020.baidu.com%3A8022%2Fbprouting%2FBpFlowRouting%3Fappindex%3Dtrue%26t%3D0.6031993324868381"
        url = loginDomain
        # first step
        r = session.get(url)
        # get lt
        lt = getlt(r.content)
        execution = getExecution(r.content)

        # second step
        user_data = {'username': username,
                     'password': password,
                     'rememberMe': 'on',
                     'execution': execution,
                     '_eventId': 'submit',
                     'type': '1',
                     'lt':  lt
        }
        r = session.post(url, data=user_data)

        # third step login success
        execution = getExecution(r.content)
        user_data = { 'execution': execution,
                      '_eventId': 'submit',
        }

        session.verify = False

        r = session.post(url, data=user_data)

        # 验证登录成功
        if(r.content.find('Bootstrap') != -1):
            logging.info("=======" + username + "=======登录成功")
            print "loin ERP success"

        url = Env.Env.login_domain_answer
        print '##########################'
        print url

        # second step
        execution = getExecution(r.content)
        user_data = {'username': username,
                     'password': password,
                     'rememberMe': 'on',
                     'execution': execution,
                     '_eventId' : 'submit',
                     'type': '1',
                     'lt':  lt
                    }
        r = session.post(url, data=user_data)

        # third step login success
        execution = getExecution(r.content)
        user_data = {"execution": execution,
                     "_eventId": "submit",
        }

        session.verify = False

        r = session.post(url, data=user_data)
        logging.info(r.content)

    except:
        logging.exception("Login Fail:")
        return 0

    return session


def getlt(str):
    lt = ""
    mo = re.search(r"lt\" value=\"(.*)\"",str)
    if mo:
        lt = mo.group(1)
    return lt

def getExecution(str):
    execution = ""
    mo = re.search(r"execution\" value=\"(.*)\"", str)
    if mo:
        execution = mo.group(1)
    return execution

def logout(loginDomain):
    session = requests.Session()
    response = session.get(loginDomain + "/bprouting/BpFlowRouting?logout=true")
    logging.info("=============退出登录")


