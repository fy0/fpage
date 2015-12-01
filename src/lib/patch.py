#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
import sys

py_ver = sys.version_info.major

if py_ver == 2:
    reload(sys)
    sys.setdefaultencoding("utf-8")
