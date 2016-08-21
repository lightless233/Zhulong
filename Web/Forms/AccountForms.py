#!/usr/bin/env python2
# coding: utf-8
# file: AccountForms.py
# time: 16-8-21 下午12:59

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email

__author__ = "lightless"
__email__ = "root@lightless.me"


class RegisterForms(Form):
    username = StringField(
        "username",
        validators=[
            DataRequired(message=u"请输入用户名"),
            Length(min=3, max=32, message=u"用户名长度：3~32个字符")
        ]
    )
    password = PasswordField(
        "password",
        validators=[
            DataRequired(message=u"请输入密码"),
            Length(min=6, max=32, message=u"密码长度：6~32个字符")
        ]
    )
    email = StringField(
        "email",
        validators=[
            Email(message=u"请输入合法的邮箱地址")
        ]
    )

