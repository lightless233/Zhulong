#!/usr/bin/env python2
# coding: utf-8
# file: APIController.py
# time: 2016/9/6 21:11

from flask import jsonify, request
from sqlalchemy import distinct

from Web import web, db
from Web.models import ZhulongSystemImages
from Utils.LoginRequire import login_required

__author__ = "lightless"
__email__ = "root@lightless.me"


@web.route("/api/v1/get_info", methods=['GET'])
@login_required
def api_get_info():

    # 获取所有的系统镜像名称
    results = ZhulongSystemImages.query.group_by(ZhulongSystemImages.op_name).all()
    op_images_info = dict()

    try:
        for res in results:
            op_images_info[res.op_name] = list()

            # 获取对应系统镜像的版本和ID信息
            versions = ZhulongSystemImages.query.filter(
                ZhulongSystemImages.op_name == res.op_name
            ).group_by(ZhulongSystemImages.version).all()

            # 整理数据
            op_images_info[res.op_name] = [dict(value=ver.id, version=ver.version) for ver in versions]
            # for ver in versions:
            #     op_images_info[res.op_name].append(dict(value=ver.id, version=ver.version))
    except Exception as e:
        return jsonify(code=1004, message=e.message)

    return jsonify(info=op_images_info, code=1001, message="Successful")


@web.route("/api/v1/create_docker", methods=["POST"])
@login_required
def api_create_docker():
    pass

