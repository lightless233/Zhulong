#!/usr/bin/env python2
# coding: utf-8
# file: APIController.py
# time: 2016/9/6 21:11
import datetime
import json

from flask import jsonify, request, g

from Web import web, db, docker_client
from Web.models import ZhulongSystemImages
from Web.models import ZhulongUserContainers
from Utils.LoginRequire import login_required
from Utils.CommonFunctions import generate_random_string

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
    container_name = request.json.get("container_name", "")

    if version_id == "":
        return jsonify(code=1004, message="系统版本选择有误")

    # 检查version_id
    system_image = ZhulongSystemImages.query.filter(ZhulongSystemImages.id == version_id).first()
    if not system_image:
        return jsonify(code=1004, message="系统版本选择有误")
    print system_image

    # 检查container name
    if container_name == "":
        return jsonify(code=1004, message="Container名称不能为空")
    container_name = g.current_user.username + "_" + container_name
    tmp = ZhulongUserContainers.query.filter(ZhulongUserContainers.container_name == container_name).first()
    if tmp:
        return jsonify(code=1004, message="Container名称重复")

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
    container = docker_client.create_container(
        image=image_name,
        ports=ports,
        name=container_name,
        host_config=docker_client.create_host_config(
            publish_all_ports=True
        )
    )
    print container
    docker_client.start(container.get("Id"))

    # 生成随机密码
    new_password = generate_random_string(12)
    # 改密码
    exec_id = docker_client.exec_create(
        container.get("Id"),
        'bash -c "echo root:{0} | chpasswd"'.format(new_password)
    )
    print exec_id
    docker_client.exec_start(exec_id.get("Id"))
    print "exec_done!"

    # 获取端口信息，改成json格式存入数据库
    # todo 多线程
    published_ports = dict()
    ssh_port = None
    for port in ports:
        response = docker_client.port(container.get("Id"), port)[0]
        published_ports[port] = response.get("HostIp") + ":" + response.get("HostPort")
        if port == 22:
            ssh_port = response.get("HostPort")
        print published_ports[port]
    published_ports = json.dumps(published_ports)

    # 插入到数据库中
    user_container = ZhulongUserContainers(
        owner_id=g.current_user.id, image_id=system_image.id, image_type=1,
        container_name=container_name, container_id=container.get("Id"), ssh_user="root",
        ssh_port=ssh_port, ssh_password=new_password, url=None,
        ports=published_ports, is_running=True,
        last_run_time=datetime.datetime.now(), last_stop_time=None
    )
    db.session.add(user_container)
    db.session.commit()

    return "123"

