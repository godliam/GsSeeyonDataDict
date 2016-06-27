#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Liam0611'


def getCode(strText, codec):
    b = bytes((ord(i) for i in strText))
    return b.decode(codec)
