#!/usr/bin/env python2
# coding: utf-8
# file: __init__.py
# time: 16-8-7 16:12

import os
import sys

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from config import DevConfig

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

db = SQLAlchemy(web)
migrate = Migrate(web, db)
CsrfProtect(web)
bcrypt = Bcrypt(web)
mail = Mail(web)

# 引入路由
from Web.Controller.System import BeforeRequestController
from Web.Controller.Frontend import IndexController
from Web.Controller.Frontend import AccountController
from Web.Controller.Frontend import HomeController
