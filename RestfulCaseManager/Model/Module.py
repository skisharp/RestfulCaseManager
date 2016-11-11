import os

from mongoengine import Document
from mongoengine import StringField

from RestfulCaseManager.util import FileOperation
from RestfulCaseManager.util import MongodbOperation


class Module(Document):
    MongodbOperation.get_connect_mongoengine()
    name = StringField(required=True)
    owner = StringField()

    def init_module(self):
        base_path = FileOperation.get_module_file_dir("demo")
        module_package_path = FileOperation.get_module_file_dir(self.name)
        os.makedirs(module_package_path)

        FileOperation.cope_files(base_path, module_package_path)

