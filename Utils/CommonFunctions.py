#!/usr/bin/env python2
# coding: utf-8
# file: CommonFunctions.py
# time: 16-8-21 下午2:27

import random
import string

__author__ = "lightless"
__email__ = "root@lightless.me"

CHAR_POOL = string.ascii_letters + string.digits


def generate_random_string(length=64):
    return "".join(random.choice(CHAR_POOL) for i in xrange(length))


