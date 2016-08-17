#!/usr/bin/env python2
# coding: utf-8
# file: models.py
# time: 2016/8/17 23:27


from Web import db

__author__ = "lightless"
__email__ = "root@lightless.me"


class ZhulongUser(db.Model):
    """
    用户表模型
    """
    __tablename__ = "zhulong_user"

    id = db.Column(db.INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    created_time = db.Column(db.DATETIME, nullable=False)
    last_login_time = db.Column(db.DATETIME, nullable=True, default=None)
    last_login_ip = db.Column(db.String(16), nullable=True, default=None)
    token = db.Column(db.String(64), nullable=True, default=None)

    def __init__(self, uid, username, email, password, created_time, last_login_time, last_login_ip, token):
        self.id = uid
        self.username = username
        self.email = email
        self.password = password
        self.created_time = created_time
        self.last_login_time = last_login_time
        self.last_login_ip = last_login_ip
        self.token = token

    def __repr__(self):
        return "<Zhulong User {id}-{username}>".format(id=self.id, username=self.username)
