#!/usr/bin/env python2
# coding: utf-8
# file: Web.py
# time: 16-8-7 16:12

from flask_script import Manager, Server

from Web import web

__author__ = "lightless"
__email__ = "root@lightless.me"

# 设置debug模式
web.debug = True

# 设置manager
manager = Manager(web)

# 添加命令
manager.add_command("runserver", Server(host="0.0.0.0"))


@manager.shell
def make_shell_context():
    return dict(web=web)


if __name__ == '__main__':
    manager.run()
