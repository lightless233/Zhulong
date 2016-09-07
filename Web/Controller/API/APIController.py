#!/usr/bin/env python2
# coding: utf-8
# file: APIController
# time: 2016/9/6 21:11

from flask import jsonify, request
from sqlalchemy import distinct

from Web import web, db
from Web.models import ZhulongOPSystem, ZhulongBaseComponents, ZhulongBaseComponentType
from Utils.LoginRequire import login_required

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route("/api/v1/get_op_systems", methods=["GET"])
@login_required
def v1_get_op_systems():
    ops = db.session.query(distinct(ZhulongOPSystem.op_name)).all()
    # 清除ops中的垃圾信息
    ops = [o[0] for o in ops]
    if ops:
        return jsonify(code=1001, message="query success.", ops=ops)
    else:
        return jsonify(code=1004, message="No available operate system.")


@web.route("/api/v1/get_op_system_versions", methods=["GET"])
@login_required
def v1_get_op_system_versions():
    """
    获取指定操作系统的版本信息
    :return: json
    """
    op = request.args.get("op", None)
    if op is None:
        return jsonify(code=1004, message="op can't be empty.")
    op_versions = ZhulongOPSystem.query.filter(ZhulongOPSystem.op_name == op).all()
    if not op_versions:
        return jsonify(code=1004, message="No available operate system.")
    versions = list()
    for v in op_versions:
        t = dict()
        t["vid"] = v.id
        t["op_name"] = v.op_name
        t["version"] = v.version
        versions.append(t)
    return jsonify(code=1001, message="query success.", versions=versions)


@web.route("/api/v1/get_base_components", methods=['GET'])
@login_required
def v1_get_base_components():
    """
    获取基础组件的信息
    :return: json
    [
        {
            "com_type": "database",
            "data": [
                {"com_name": "MySQL", versions:["5.7", "5.6"]},
                {"com_name": "SQLite", versions:["2.1", "3.0"]},
            ],
        },
        ...
    ]
    """
    result = db.session.query(
        ZhulongBaseComponents.components_name,
        ZhulongBaseComponents.components_version,
        ZhulongBaseComponentType.type_name,
    ).filter(
        ZhulongBaseComponents.components_type == ZhulongBaseComponentType.id
    ).all()
    print result
    # 整理数据
    return_list = list()
    for info in result:
        # 检查return_list中是否存在对应类型的字典
        found = False
        for dd in return_list:
            if dd.get("com_type") == info[2]:
                found = True
                # 找到了，直接向data中添加数据
                # 检查dd中是否存在该类型的组件
                f_found = False
                for c in dd["data"]:
                    if c.get("com_name") == info[0]:
                        # 找到了，添加版本信息
                        f_found = True
                        c["versions"].append(info[1])
                        break
                if not f_found:
                    dd["data"].append(dict(com_name=info[0], versions=[info[1]]))
                break
        else:
            return_list.append(dict(com_type=info[2], data=[dict(com_name=info[0], versions=[info[1]])]))

    return jsonify(code=1001, data=return_list)

