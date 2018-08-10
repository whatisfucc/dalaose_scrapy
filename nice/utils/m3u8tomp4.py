#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: fzk
# @Time  13:40

import os

path = '/Users/dzsbhmacbookair/python_pro/nice/films'
menu = os.listdir(path)
for dp, dn, fs in os.walk(path):
    if 'index.m3u8' in fs:
        os.chdir(dp)
        os.system('ffmpeg -allowed_extensions ALL -c copy {0}.mp4 -i index.m3u8'.format(dp.split('/')[-1]))
