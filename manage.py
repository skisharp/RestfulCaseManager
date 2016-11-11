#!/usr/bin/env python
import os
import sys
import log

if __name__ == "__main__":
    #init log
    log.log_setting()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RestfulCaseManager.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
