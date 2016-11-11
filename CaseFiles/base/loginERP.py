# coding: UTF-8

import requests
import re
import json
import sys



def login(domain,username,password):

    session = None
    try:
        session = requests.Session()
        # url = domain + "/login?service=http%3A%2F%2Ferp8020.baidu.com%3A8022%2Fbprouting%2FBpFlowRouting%3Fappindex%3Dtrue%26t%3D0.6031993324868381"
        url = domain
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
                            "_eventId": "submit",
                            "setCookiePathSuccess":"http://api.erp8030.baidu.com/erpsso/passport",
                            "setCookiePathSuccess":"http://api.fusion8030.baidu.com/erpsso/passport"
        }


        session.verify = False

        r = session.post(url, data=user_data)


        # 验证登录成功
        if(r.content.find('Bootstrap') != -1):
            print "loin ERP success"

    except Exception,e:
        print '发生错误：',
        print str(e)
        print "登录不成功！退出程序"
        sys.exit(1)


    return session



def getlt(str):
    lt = ""
    mo = re.search(r"lt\" value=\"(.*)\"",str)
    if mo:
        lt = mo.group(1)
    return lt

def getExecution():
    execution = ""
    mo = re.search(r"execution\" value=\"(.*)\"", str)
    if mo:
        lt = mo.group(1)
    return execution




def logout(loginDomain):
    session = requests.Session()
    response = session.get(loginDomain + "/bprouting/BpFlowRouting?logout=true")


