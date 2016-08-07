#!/usr/bin/env python2
# coding: utf-8
# file: IndexController.py
# time: 16-8-7 下午4:25

from Web import web

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route("/", methods=["GET"])
@web.route("/index", methods=["GET"])
def index():
    return "index"
