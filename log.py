import logging
import os

from RestfulCaseManager import settings


def log_setting():
    logfile = os.path.join(settings.BASE_DIR, 'log')
    logfile = os.path.join(logfile, "myapp.log")

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=logfile,
                        filemode='w')

