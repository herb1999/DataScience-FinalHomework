#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import jsonify
def ResponseOK(data=''):
    res = {
        'code': 0,
        'data': data
    }
    return jsonify(res)