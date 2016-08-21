#!/usr/bin/env python2
# coding: utf-8
# file: CommonFunctions.py
# time: 16-8-21 下午2:27

import random
import string
import hashlib

from flask_mail import Message

from Web import web
from Web import mail

__author__ = "lightless"
__email__ = "root@lightless.me"

CHAR_POOL = string.ascii_letters + string.digits


def generate_random_string(length=64):
    """
    生成随机字符串
    :param length: 字符串长度，默认64个字符
    :return: 生成好的随机字符串
    """
    return "".join(random.choice(CHAR_POOL) for i in xrange(length))


def generate_confirm_token(username, email, user_token):
    return hashlib.sha512("..".join([user_token, username, email])).hexdigest()


def confirm_email_token(token, username, email, user_token):
    return token == hashlib.sha512("..".join([user_token, username, email])).hexdigest()


def send_mail(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=web.config["MAIL_DEFAULT_SENDER"]
    )
    mail.send(msg)


