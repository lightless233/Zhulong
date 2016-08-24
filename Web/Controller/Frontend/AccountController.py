#!/usr/bin/env python2
# coding: utf-8
# file: AccountController.py
# time: 2016/8/19 23:19

import datetime

from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from sqlalchemy.sql.expression import or_
from sqlalchemy.exc import SQLAlchemyError

from Web import web
from Web import db
from Web.Forms.AccountForms import RegisterForms
from Web.models import ZhulongUser
from Utils.CommonFunctions import generate_confirm_token
from Utils.CommonFunctions import confirm_email_token
from Utils.CommonFunctions import send_mail

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route("/account/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass
    else:
        return render_template("Frontend/Account/login.html")


@web.route("/account/register", methods=["GET", "POST"])
def register():

    register_form = RegisterForms()

    if request.method == "GET":
        return render_template("Frontend/Account/register.html")
    elif request.method == "POST":
        if register_form.validate_on_submit():

            # 查询是否有已经存在的用户名或邮箱
            tmp_user = ZhulongUser.query.filter(
                or_(
                    ZhulongUser.username == register_form.username.data,
                    ZhulongUser.email == register_form.email.data
                )
            ).first()
            if tmp_user:
                return jsonify(tag="danger", msg="用户名或邮箱已经存在")

            # 生成新的用户
            new_user = ZhulongUser(
                username=register_form.username.data,
                password=register_form.password.data,
                email=register_form.email.data,
                created_time=datetime.datetime.now(),
                last_login_time=None,
                last_login_ip=request.remote_addr,
            )
            try:
                # 插入数据库
                db.session.add(new_user)

                # 发送邮件
                token = generate_confirm_token(new_user.username, new_user.email, new_user.token)
                confirm_url = url_for("confirm_email", token=token, user=new_user.username, _external=True)
                subject = u"[烛龙] 请确认你的邮箱地址"
                html = render_template("confirm_email.html", confirm_url=confirm_url)
                send_mail(new_user.email, subject, html)

                # 提交修改
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


@web.route("/account/confirm_email/token/<token>/user/<user>", methods=["GET"])
def confirm_email(token, user):

    return_data = dict(tag="danger", msg=None)

    # 检查参数
    if token is None or user is None:
        return_data["msg"] = u"参数错误"
        return render_template("Frontend/Account/confirm_email.html", data=return_data)

    # 检查该用户是否已经激活
    u = ZhulongUser.query.filter(ZhulongUser.username == user).first()
    if u.is_active:
        return_data["msg"] = u"已经激活过了，请登录！"
        return render_template("Frontend/Account/confirm_email.html", data=return_data)

    # 验证token
    result = confirm_email_token(token, user, u.email, u.token)
    if result:
        # 验证成功
        try:
            u.is_active = True
            db.session.add(u)
            db.session.commit()
            return_data["tag"] = "success"
            return_data["msg"] = u"验证成功！请登录！"
            return render_template("Frontend/Account/confirm_email.html", data=return_data)
        except SQLAlchemyError:
            return_data["msg"] = u"服务器开小差了，请稍后再试！"
            return render_template("Frontend/Account/confirm_email.html", data=return_data)
    else:
        # 验证失败
        return_data["msg"] = u"验证失败！"
        return render_template("Frontend/Account/confirm_email.html", data=return_data)
