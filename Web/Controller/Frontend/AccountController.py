#!/usr/bin/env python2
# coding: utf-8
# file: AccountController.py
# time: 2016/8/19 23:19

from flask import render_template
from flask import request

from Web import web

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route("/login", methods=["GET", "POST"])
def login():
    pass


@web.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("Frontend/Account/register.html")
    elif request.method == "POST":

        # 获取数据
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")


