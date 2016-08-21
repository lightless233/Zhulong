#!/usr/bin/env python2
# coding: utf-8
# file: AccountController.py
# time: 2016/8/19 23:19

import datetime

from flask import render_template
from flask import request
from flask import jsonify
from sqlalchemy.sql.expression import or_

from Web import web
from Web import db
from Web.Forms.AccountForms import RegisterForms
from Web.models import ZhulongUser

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route("/account/login", methods=["GET", "POST"])
def login():
    pass


@web.route("/account/register", methods=["GET", "POST"])
def register():

    register_form = RegisterForms()

    if request.method == "GET":
        return render_template("Frontend/Account/register.html")
    elif request.method == "POST":
        if register_form.validate_on_submit():

            tmp_user = ZhulongUser.query.filter(
                or_(
                    ZhulongUser.username == register_form.username.data,
                    ZhulongUser.email == register_form.email.data
                )
            ).first()
            if tmp_user:
                return jsonify(tag="danger", msg="用户名或邮箱已经存在")

            new_user = ZhulongUser(
                username=register_form.username.data,
                password=register_form.password.data,
                email=register_form.email.data,
                created_time=datetime.datetime.now(),
                last_login_time=None,
                last_login_ip=request.remote_addr,
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return jsonify(tag="success", msg="注册成功，请验证邮箱地址！")
            except Exception as e:
                return jsonify(tag="danger", msg=e)
        else:
            for field_name, error_message in register_form.errors.iteritems():
                print field_name, error_message
                for error in error_message:
                    print error
                    return jsonify(tag="danger", msg=error)



