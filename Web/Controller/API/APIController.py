#!/usr/bin/env python2
# coding: utf-8
# file: APIController
# time: 2016/9/6 21:11

from flask import jsonify, request
from sqlalchemy import distinct

from Web import web, db
from Web.models import ZhulongOPSystem

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route("/api/v1/get_op_systems", methods=["GET"])
def v1_get_op_systems():
    ops = db.session.query(distinct(ZhulongOPSystem.op_name)).all()
    # 清除ops中的垃圾信息
    ops = [o[0] for o in ops]
    if ops:
        return jsonify(code=1001, message="query success.", ops=ops)
    else:
        return jsonify(code=1004, message="No available operate system.")


@web.route("/api/v1/get_op_system_versions", methods=["GET"])
def v1_get_op_system_versions():
    """
    获取指定操作系统的版本信息
    :return: json
    """
    op = request.args.get("op", None)
    if op is None:
        return jsonify(code=1004, message="op can't be empty.")
    op_versions = ZhulongOPSystem.query.filter(ZhulongOPSystem.op_name == op).all()
    if not len(op_versions):
        return jsonify(code=1004, message="No available operate system.")
    versions = list()
    for v in op_versions:
        t = dict()
        t["vid"] = v.id
        t["op_name"] = v.op_name
        t["version"] = v.version
        versions.append(t)
    return jsonify(code=1001, message="query success.", versions=versions)


