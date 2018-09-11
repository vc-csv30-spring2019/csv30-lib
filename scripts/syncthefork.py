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
    return [file_obj.close(), text] if run else [0, ""]


def check_for_uncommitted_changes():
    res, text = use('git diff-index --quiet HEAD --', True)
    return res is None


def check_if_pull_needed():
    res, text = use('git fetch', True)
    if res is not None:
        log(CRITICAL, "Unable to fetch repo ({}): ".format(res) + text)
        sys.exit(res)
    res, head_rev = use('git rev-parse HEAD', True)
    if res is not None:
        log(CRITICAL, "Unable to get HEAD revision ({}): ".format(res) + text)
        sys.exit(res)
    res, remote_rev = use('git rev-parse @{u}', True)
    if res is not None:
        log(CRITICAL, "Unable to get remote revision ({}): ".format(res) + text)
        sys.exit(res)
    return head_rev.strip() != remote_rev.strip()


def check_for_upstream_remote():
    res, text = use('git remote get-url ' + UPSTREAM_NAME, True)
    return res is None


def add_upstream_remote():
    res, text = use('git remote add ' + UPSTREAM_NAME + ' ' + UPSTREAM_URL, True)
    if res is not None:
        log(CRITICAL, 'Unable to add upstream remote ({}): '.format(res) + text )
        sys.exit(res)
    return True


def sync_the_fork():
    res, text = use('git fetch ' + UPSTREAM_NAME, True)
    if res is not None:
        log(CRITICAL, 'Unable to fetch remote upstream ({}): '.format(res) + text)
        sys.exit(res)
    res, text = use('git checkout master', True)
    if res is not None:
        log(CRITICAL, 'Unable to checkout master branch ({}): '.format(res) + text)
        sys.exit(res)
    res, text = use('git rebase ' + UPSTREAM_NAME + '/master', True)
    if res is not None:
        log(CRITICAL, 'Rebase of upstream/master failed ({}): '.format(res) + text)
        sys.exit(res)
    return True

GITHUB_URL = 'https://www.github.com/'
REPO_NAME = (project.ASSIGNMENT_NUM + '-' + project.ASSIGNMENT_NAME).lower()
UPSTREAM_URL = GITHUB_URL + project.GITHUB_ORGANIZATION + '/' + REPO_NAME
UPSTREAM_NAME = 'upstream'

log(INFO, 'Checking for uncommitted changes...')
result = check_for_uncommitted_changes()
if not result:
    log(ERROR, 'Uncommitted changes exist. Commit and push before running this script again')
    sys.exit(1)
log(INFO, 'Done.')

log(INFO, 'Checking if you need to pull...')
result = check_if_pull_needed()
if result:
    log(ERROR, 'You must pull changes from your repository before running this script again')
    sys.exit(1)
log(INFO, 'Done.')

log(INFO, 'Checking for upstream remote')
result = check_for_upstream_remote()
if not result:
    add_upstream_remote()
log(INFO, 'Done.')

log(INFO, 'Syncing the fork...')
result = sync_the_fork()
if result:
    log(DEBUG, 'Fork has been succesfully synced with the repo it was forked from')
else:
    log(CRITICAL, 'Unable to sync the fork')
log(INFO, 'Done.')