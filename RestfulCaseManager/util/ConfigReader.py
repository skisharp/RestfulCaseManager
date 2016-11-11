# -* - coding: UTF-8 -* -
import ConfigParser
import os
import logging
from RestfulCaseManager.util import FileOperation


def read_conf(module):
    config_parser = ConfigParser.ConfigParser()

    config_dir = FileOperation.get_module_file_dir(module)
    config_file_path = os.path.join(config_dir, "config.cfg")

    logging.info(config_file_path)
    try:
        config_parser.read(config_file_path)
    except IOError:
        logging.info("Could not read config file!")
    except:
        logging.info("Handle file error!")

    return config_parser



