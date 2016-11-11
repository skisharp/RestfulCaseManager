# -*- coding: utf-8 -*-
from pymongo import MongoClient
import logging
import traceback
from mongoengine import connect

# 连接到mongodb数据库，如果不成功显示 NO data
def getMongodb():
    assessDB = None
    try:
        mongoClient = MongoClient("mongodb://localhost:11111/")
        if mongoClient:
            assessDB = mongoClient["assess"]
            logging.info("Connect to mogodb success!")

        else:
            logging.info("Connect to mongodb fail!")
    except Exception,e:
        logging.error("Error:Connect to mongodb fail! ")
        logging.error(traceback.print_exc())

    return assessDB


def get_connect_mongoengine():
    connect('assess', host='mongodb://localhost:11111/')






