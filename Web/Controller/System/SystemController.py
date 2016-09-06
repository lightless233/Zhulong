#!/usr/bin/env python2
# coding: utf-8
# file: SystemController.py
# time: 16-8-25 上午12:03

from flask import g, session, render_template

from Web import web
from Web.models import ZhulongUser

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.before_request
def before_request():
    """
    每个请求前获取用户信息并挂到g变量上
    """
    if "username" in session:
        g.current_user = ZhulongUser.query.filter(ZhulongUser.username == session["username"]).first()


@web.route("/tpl/<path:path>")
def get_tpl(path):
    return render_template(path)
