#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: fzk
# @Time  10:55

import hashlib


def md5(string):
    m = hashlib.md5()
    m.update(string.encode('utf8'))
    return m.hexdigest()
