# -*- coding: utf-8 -*-
from RestfulCaseManager.util import ConfigReader

userNamesDict = {}
userPasswordsDict = {}

def initUsers(env):
    config = ConfigReader.read_conf()
    section = "users"
    roles = config.options(section)

    # 密码后缀
    try:
        passwordPostfix = config.get("passwordpostfix",env)
        if passwordPostfix == "empty":
            passwordPostfix = ""
    except :
        passwordPostfix = ""

    # 初始化用户密码列表
    for role in roles:
        userNamesDict[role] = config.get(section,role)
        userPasswordsDict[role] = config.get(section,role) + passwordPostfix




