#!/usr/bin/env python2
# coding: utf-8
# file: __init__.py
# time: 16-8-7 16:12

import os
import sys

import docker
from docker.errors import DockerException, APIError
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_triangle import Triangle

from config import DevConfig
from Utils.LoggerHelp import logger

__author__ = "lightless"
__email__ = "root@lightless.me"


# 设置编码为UTF-8
reload(sys)
sys.setdefaultencoding('utf-8')

# 获取templates和static目录
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# 初始化Flask app
web = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
web.config.from_object(DevConfig)
web.debug = True

# 初始化相关插件
db = SQLAlchemy(web)
migrate = Migrate(web, db)
CsrfProtect(web)
bcrypt = Bcrypt(web)
mail = Mail(web)
triangle = Triangle(web)

# 初始化docker remote api
docker_remote_api_url = web.config.get("DOCKER_REMOTE_API_URL", None)
if docker_remote_api_url is None:
    logger.error("Docker Remote API没有设置")
    sys.exit(1)
try:
    logger.info("Try to connect to docker remote api...")
    docker_client = docker.Client(base_url=docker_remote_api_url, timeout=30)
    logger.info("Connect successful.")
    docker_version = docker_client.version()
    logger.info("Docker Version: {}".format(docker_version.get("Version", "Unknown")))
    logger.info("OS: {0} {1} {2}".format(
        docker_version.get("Os", "Unknown OS"),
        docker_version.get("Arch", "Unknown Arch"),
        docker_version.get("KernelVersion", "Unknown Kernel")
    ))
except (DockerException, APIError) as e:
    logger.error(e)
    logger.fatal("Docker Remote API connect failed.")
    sys.exit(1)

# 引入路由
from Web.Controller.System import SystemController
from Web.Controller.Frontend import IndexController
from Web.Controller.Frontend import AccountController
from Web.Controller.Frontend import HomeController
from Web.Controller.API import APIController
