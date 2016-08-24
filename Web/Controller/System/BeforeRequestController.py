#!/usr/bin/env python2
# coding: utf-8
# file: BeforeRequestController.py
# time: 16-8-25 上午12:03

from flask import g, session

from Web import web
from Web.models import ZhulongUser

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.before_request
def before_request():
    if "username" in session:
        g.current_user = ZhulongUser.query.filter(ZhulongUser.username == session["username"]).first()
