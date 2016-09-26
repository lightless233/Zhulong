#!/usr/bin/env python2
# coding: utf-8
# file: models.py
# time: 2016/8/17 23:27

import datetime

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
    last_login_time = db.Column(db.DATETIME, nullable=True, default=None)
    last_login_ip = db.Column(db.String(16), nullable=True, default=None)
    token = db.Column(db.String(64), nullable=True, default=None)
    blocked = db.Column(db.BOOLEAN, nullable=True, default=False)
    is_active = db.Column(db.BOOLEAN, nullable=False, default=False)
    created_time = db.Column(db.DATETIME, nullable=False)
    updated_time = db.Column(db.DATETIME, nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def valid_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, username, email, password, last_login_time, last_login_ip, created_time, updated_time):
        # TODO: fix this
        self.username = username
        self.email = email
        self.set_password(password)
        self.created_time = created_time
        self.updated_time = updated_time
        self.last_login_time = last_login_time
        self.last_login_ip = last_login_ip
        self.token = generate_random_string(64)
        self.is_active = False
        self.blocked = False

    def __repr__(self):
        return "<Zhulong User {id}-{username}>".format(id=self.id, username=self.username)


class ZhulongUserContainers(db.Model):
    """
    记录用户创建的docker containers
    包括正在运行的以及已经停止的
    """
    __tablename__ = "zhulong_user_containers"

    id = db.Column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    owner_id = db.Column(INTEGER(10, unsigned=True), nullable=True, default=None)   # container拥有者ID
    image_id = db.Column(INTEGER(10, unsigned=True), nullable=True, default=None)   # image的ID
    image_type = db.Column(TINYINT(2, unsigned=True), nullable=True, default=None)  # image type, 1-base, 2-user
    container_name = db.Column(db.String(64), nullable=True, default=None)          # container的名称
    container_id = db.Column(db.String(12), nullable=True, default=None)            # container ID
    ssh_user = db.Column(db.String(32), nullable=True, default=None)                # SSH username
    ssh_port = db.Column(db.INTEGER(5), nullable=True, default=None)                # SSH port
    ssh_password = db.Column(db.String(16), nullable=True, default=None)            # SSH password
    url = db.Column(db.String(255), nullable=True, default=None)                    # 分配到的域名
    is_running = db.Column(db.BOOLEAN, nullable=True, default=False)        # container是否在运行，1-run，0-stop状态
    is_deleted = db.Column(db.BOOLEAN, nullable=True, default=False)        # 该container是否被删除，1-删了，0-没删
    last_run_time = db.Column(db.DATETIME, nullable=True, default=None)     # 最后一次run时间
    last_stop_time = db.Column(db.DATETIME, nullable=True, default=None)    # 最后一次stop时间
    created_time = db.Column(db.DATETIME, nullable=True, default=None)
    updated_time = db.Column(db.DATETIME, nullable=True, default=None)

    def __init__(self, owner_id, docker_name, docker_description, created_time, updated_time):
        # TODO: fix this
        self.owner_id = owner_id
        self.docker_name = docker_name
        self.docker_description = docker_description
        self.created_time = created_time
        self.updated_time = updated_time

    def __repr__(self):
        return "<ZhulongUserContainers {0}-{1}-{2}>".format(self.id, self.container_name, self.container_id)


class ZhulongSystemImages(db.Model):
    """
    存储基础操作系统的images
    提供给用户在此环境上进行搭建工作
    """
    __tablename__ = "zhulong_system_images"

    id = db.Column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    op_name = db.Column(db.String(32), nullable=True, default=None)        # 操作系统名称
    version = db.Column(db.String(32), nullable=True, default=None)        # 版本
    image_name = db.Column(db.String(32), nullable=True, default=None)     # 镜像名称 e.g. base-ubuntu:16.04
    image_id = db.Column(db.String(12), nullable=True, default=None)       # 镜像id
    expose_port = db.Column(db.String(512), nullable=True, default=None)   # 需要暴露的端口，逗号分隔: 22,80,443
    is_deleted = db.Column(db.BOOLEAN, nullable=True, default=None)
    created_time = db.Column(db.DATETIME, nullable=True, default=None)
    updated_time = db.Column(db.DATETIME, nullable=True, default=None)

    def __init__(self, op_name=None, version=None, image_name=None,
                 image_id=None, expose_port=None, is_deleted=None,
                 created_time=datetime.datetime.now(), updated_time=datetime.datetime.now()):
        self.op_name = op_name
        self.version = version
        self.image_name = image_name
        self.image_id = image_id
        self.expose_port = expose_port
        self.is_deleted = is_deleted
        self.created_time = created_time
        self.updated_time = updated_time

    def __repr__(self):
        return "<ZhulongSystemImages {0}-{1}>".format(self.id, self.image_name)


class ZhulongUserImages(db.Model):
    """
    用户制作好的image
    可以继续制作，也可以发布到市场中
    """
    __tablename__ = "zhulong_shared_images"

    id = db.Column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    owner_id = db.Column(INTEGER(10, unsigned=True), default=None)    # image的拥有者
    image_id = db.Column(db.String(12), default=None)       # image id
    image_name = db.Column(db.String(32), default=None)     # image name, e.g. base-ubuntu:16.04
    image_description = db.Column(db.String(255), default=None)     # image 描述
    exposed_port = db.Column(db.String(512), default=None)  # 需要暴露的端口，逗号分隔: 22,80,443
    parent_image = db.Column(db.String(512), default=None)  # 父image id，逗号分隔： 123,452，只存储UserImage
    is_shared = db.Column(db.BOOLEAN, default=False)        # 是否发布到市场，true-发布，false-不发布
    is_locked = db.Column(db.BOOLEAN, default=False)        # 是否锁定，如果锁定则不允许其他人再发布
    is_deleted = db.Column(db.BOOLEAN, default=False)
    created_time = db.Column(db.DATETIME, default=None)
    updated_time = db.Column(db.DATETIME, default=None)

    def __init__(self, owner_id=None, image_id=None, image_name=None, image_description=None,
                 exposed_port=None, parent_image=None, is_shared=False, is_locked=False, is_deleted=False,
                 created_time=datetime.datetime.now(), updated_time=datetime.datetime.now()):
        self.owner_id = owner_id
        self.image_id = image_id
        self.image_name = image_name
        self.image_description = image_description
        self.exposed_port = exposed_port
        self.parent_image = parent_image
        self.is_shared = is_shared
        self.is_locked = is_locked
        self.is_deleted = is_deleted
        self.created_time = created_time
        self.updated_time = updated_time

    def __repr__(self):
        return "<ZhulongUserImages {0}-{1}>".format(self.id, self.image_name)

    # TODO: add two function: 1.add_expose_port, 2.add_parent_image
    # TODO: change primary key to BIGINT(20) UNSIGNED
