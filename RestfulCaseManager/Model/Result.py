from mongoengine import *


class Result(Document):
    connect('assess', host='mongodb://localhost:11111/')
    case_id = ObjectIdField()
    result = StringField()
    actual_result = StringField()
    expect_result = StringField()
    response_status = StringField()
    response_content = StringField()
    batch_id=ObjectIdField()
    running_log = StringField()

