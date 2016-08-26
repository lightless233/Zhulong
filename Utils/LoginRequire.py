#!/usr/bin/env python2
# coding: utf-8
# file: LoginRequire.py
# time: 16-8-26 下午10:49

from functools import wraps
from flask import g, request, redirect, url_for, session

__author__ = "lightless"
__email__ = "root@lightless.me"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username", None) is None:
            return redirect(url_for('account_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

