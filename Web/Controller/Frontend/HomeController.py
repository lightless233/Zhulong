#!/usr/bin/env python2
# coding: utf-8
# file: HomeController.py
# time: 16-8-24 下午11:39

from flask import g

from Utils.LoginRequire import login_required
from Web import web

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route("/home/index")
@login_required
def home_index():
    return g.current_user.username
