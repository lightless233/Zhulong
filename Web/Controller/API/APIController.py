#!/usr/bin/env python2
# coding: utf-8
# file: APIController.py
# time: 2016/9/6 21:11

from flask import jsonify, request

from Web import web, db, docker_client
from Web.models import ZhulongSystemImages
from Web.models import ZhulongUserContainers
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
    print request.json
    exposed_port = request.json.get("port", "")
    version_id = request.json.get("version_id", "")

    if version_id == "":
        return jsonify(code=1004, message="系统版本选择有误")

    # 检查version_id
    system_image = ZhulongSystemImages.query.filter(ZhulongSystemImages.id == version_id).first()
    if not system_image:
        return jsonify(code=1004, message="系统版本选择有误")
    print system_image

    # 整理port
    try:
        ports = [int(p.strip()) for p in exposed_port.split(",")]
    except ValueError:
        return jsonify(code=1004, message="端口填写有误")
    print ports

    # 默认开启22端口
    if 22 not in ports:
        ports.append(22)

    # 调用docker API跑起container
    image_name = system_image.image_name
    container_id = docker_client.create_container(
        image=image_name,
        ports=ports,
        host_config=docker_client.create_host_config(
            publish_all_ports=True
        )
    )
    print container_id
    # 插入到数据库中

    return "123"

