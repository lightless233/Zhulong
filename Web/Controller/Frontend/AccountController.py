#!/usr/bin/env python2
# coding: utf-8
# file: AccountController.py
# time: 2016/8/19 23:19

from flask import render_template

from Web import web

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route("/login", methods=["GET", "POST"])
def login():
    pass


@web.route("/register", methods=["GET", "POST"])
def register():
    return render_template("Frontend/Account/register.html")

