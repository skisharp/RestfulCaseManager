# coding: utf-8
import logging
import os
import json

from RestfulCaseManager.util import FileOperation


class RoleUserMapper():

    # 得到所有的角色和用户名
    @classmethod
    def getRoleUserDict(cls, module):
        roleUserJson = None
        try:
            configDir = FileOperation.get_module_file_dir(module)
            roleUserFilePath = os.path.join(configDir, "RoleUserMapper.json")
            roleUserFile = open(roleUserFilePath, 'r')
            roleUserJson = json.load(roleUserFile)

            logging.info('读取角色文件成功！')
        except:
            logging.exception("读取角色文件失败：")

        RoleUserMapper.roleUserJson = roleUserJson
        RoleUserMapper.Roles = roleUserJson.keys()

        return roleUserJson
