#!/usr/bin/env python2
# coding: utf-8
# file: models.py
# time: 2016/8/17 23:27

from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.dialects.mysql import TINYINT

from Utils.CommonFunctions import generate_random_string
from Web import db
from Web import bcrypt

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
    is_active = db.Column(db.BOOLEAN, nullable=False, default=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def valid_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, username, email, password, created_time, last_login_time, last_login_ip):
        self.username = username
        self.email = email
        self.set_password(password)
        self.created_time = created_time
        self.last_login_time = last_login_time
        self.last_login_ip = last_login_ip
        self.token = generate_random_string(64)
        self.is_active = False

    def __repr__(self):
        return "<Zhulong User {id}-{username}>".format(id=self.id, username=self.username)


class ZhulongDocker(db.Model):
    """
    Docker表模型，记录用户创建的docker
    """
    __tablename__ = "zhulong_docker"

    id = db.Column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    owner_id = db.Column(INTEGER(10, unsigned=True), nullable=True, default=None)
    docker_name = db.Column(db.String(32), nullable=True, default=None, index=True)
    docker_description = db.Column(db.String(128), nullable=True, default=None)
    shared = db.Column(db.BOOLEAN, nullable=True, default=True)
    created_time = db.Column(db.DATETIME, nullable=True, default=None)
    updated_time = db.Column(db.DATETIME, nullable=True, default=None)

    def __init__(self, owner_id, docker_name, docker_description, created_time, updated_time):
        self.owner_id = owner_id
        self.docker_name = docker_name
        self.docker_description = docker_description
        self.created_time = created_time
        self.updated_time = updated_time

    def __repr__(self):
        return "<Zhulong Docker {id}-{docker_name}>".format(id=self.id, docker_name=self.docker_name)


class ZhulongDockerInfo(db.Model):
    """
    记录每个docker的详细信息
    """
    __tablename__ = "zhulong_docker_info"

    id = db.Column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    docker_id = db.Column(INTEGER(10, unsigned=True), nullable=True, default=None)
    docker_tag = db.Column(db.String(64), nullable=True, default=None)
    docker_image_id = db.Column(db.String(12), nullable=True, default=None)
    op_system = db.Column(TINYINT(unsigned=True), nullable=True, default=None)
    ssh_port = db.Column(INTEGER(5, unsigned=True), nullable=True, default=None)
    ssh_password = db.Column(db.String(16), nullable=True, default=None)
    ssh_user = db.Column(db.String(32), nullable=True, default="root")
    ip = db.Column(db.String(16), nullable=True, default=None)
    url = db.Column(db.String(256), nullable=True, default=None)
    last_start_time = db.Column(db.DATETIME, nullable=True, default=None)

    def __init__(self, docker_id, docker_tag, docker_image_id, op_system,
                 ssh_port, ssh_password, ssh_user, ip, url, last_start_time):
        self.docker_id = docker_id
        self.docker_tag = docker_tag
        self.docker_image_id = docker_image_id
        self.op_system = op_system
        self.ssh_port = ssh_port
        self.ssh_password = ssh_password
        self.ssh_user = ssh_user
        self.ip = ip
        self.url = url
        self.last_start_time = last_start_time

    def __repr__(self):
        return "<ZhulongDockerInfo docker id:{id}-{tag}>".format(id=self.docker_id, tag=self.docker_tag)


class ZhulongOPSystem(db.Model):
    """
    存储docker的系统镜像信息
    """
    __tablename__ = "zhulong_op_system"

    id = db.Column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    op_name = db.Column(db.String(32), nullable=False, default=None)
    image_name = db.Column(db.String(32), nullable=False, default=None)
    image_url = db.Column(db.String(32), nullable=False, default=None)

    def __init__(self, op_name, image_name, image_url):
        self.op_name = op_name
        self.image_name = image_name
        self.image_url = image_url

    def __repr__(self):
        return "<ZhulongOPSystem {id}-{op_name}>".format(id=self.id, op_name=self.op_name)
