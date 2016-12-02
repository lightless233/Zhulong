#!/usr/bin/env python2
# coding: utf-8
# file: AccountForms.py
# time: 16-8-21 下午12:59

from dns.resolver import query
from dns.exception import DNSException

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from wtforms import ValidationError

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

    @staticmethod
    def validate_username(form, field):
        if not field.data.isalnum():
            raise ValidationError(u"用户名只允许数字和字母")

    @staticmethod
    def validate_email(form, field):
        domain = field.data.strip().split("@")[-1]
        try:
            query(domain, "MX")
        except DNSException:
            raise ValidationError(u"请输入合法的邮箱")


class LoginForms(Form):
    username_or_email = StringField(
        "username_or_email",
        validators=[
            DataRequired(message=u"请输入用户名或邮箱"),
        ]
    )

    password = PasswordField(
        "password",
        validators=[
            DataRequired(message=u"请输入密码"),
            Length(min=6, max=32, message=u"密码长度：6~32个字符")
        ]
    )

    @staticmethod
    def validate_username_or_email(form, field):
        if "@" in field.data:
            # 输入了email
            try:
                # email = field.data.encode('utf-8')
                domain = field.data.strip().split("@")[-1]
                query(domain, "MX")
            except DNSException:
                raise ValidationError(u"请输入合法的邮箱")
        else:
            # 输入了用户名
            if not field.data.isalnum():
                raise ValidationError(u"用户名只允许数字和字母")
            if not (3 < len(field.data) < 32):
                raise ValidationError(u"用户名长度为3~32个字符")

