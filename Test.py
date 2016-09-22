#!/usr/bin/env python2
# coding: utf-8
# file: Test.py
# time: 2016/7/26 20:48

from Web import docker_client

__author__ = "lightless"
__email__ = "root@lightless.me"


print docker_client.pull(repository="busybox", tag="latest")

# container_id = docker_client.create_container(
#     "busybox", "cat /etc/passwd", ports=[1111, 2222],
#     host_config=docker_client.create_host_config(
#         port_bindings={
#             1111: 4567,
#             2222: None
#         }
#     )
# )
# print container_id
# docker_client.start(container_id["Id"])
# print docker_client.logs(container=container_id["Id"], stdout=True, stderr=True)

