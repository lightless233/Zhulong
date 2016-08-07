#!/usr/bin/env python2
# coding: utf-8
# file: __init__.py
# time: 16-8-7 16:12

import sys

from flask import Flask
from flask_script import Manager, Server

__author__ = "lightless"
__email__ = "root@lightless.me"


reload(sys)
sys.setdefaultencoding('utf-8')

web = Flask(__name__)
manager = Manager(web)
manager.add_command("runserver", Server(host="0.0.0.0"))


from Web.Controller.Frontend import IndexController

