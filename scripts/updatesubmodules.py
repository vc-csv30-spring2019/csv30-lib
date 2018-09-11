#!/usr/bin/python

import sys
sys.path.append(".githooks/")

import os

import project

CRITICAL = 0
ERROR = 1
WARNING = 8
DEBUG = 9
INFO = 10

DEBUG_LEVEL = 11


def log(level, msg):
    if level <= DEBUG_LEVEL:
        print msg


def use(command, run=False):
    if not run:
        print command
    else:
        file_obj = os.popen(command)
        text = file_obj.read()
    return [file_obj.close(), text] if run else [None, ""]

def update_submodules():
    res, text = use('git submodule update --remote', True)
    if res is not None:
        log(CRITICAL, 'Unable to update submodules ({}): '.format(res) + text)
        sys.exit(res)
    return True

log(INFO, 'Updating submodules...')
result = update_submodules()
log(INFO, 'Done.')