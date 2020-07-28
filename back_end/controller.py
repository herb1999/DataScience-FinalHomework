#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Flask
from flask import Flask,url_for,request,render_template
from flask_cors import CORS
from flask import jsonify
from flask import request
from src.util import *
from back_end.reponseHelper import *
from back_end.service import *
from src.rating import checkTestCode
app = Flask(__name__)
CORS(app, supports_credentials=True)
CORS(app, resources=r'/*')

# @app.route('/test', methods=['GET'])
# def test():
#     print('recieved')
#     return 'hhh'

@app.route('/caseMd',methods=['GET'])
def caseMd():
    caseId = request.args.get('caseId')
    print('caseId',caseId)

    data=getMd(caseId)

    return ResponseOK(data)

@app.route('/allCases',methods=['GET'])
def allCases():
    return ResponseOK(getAllCases())

@app.route('/commitCode',methods=['POST'])
def commitCode():
    data = json.loads(request.get_data(as_text=True))
    caseId = data['caseId']
    code = data['code']
    print(data)

    saveCode(caseId,code)
    res=checkTestCode(caseId,code)
    return ResponseOK(res)

@app.route('/recommendLabel',methods=['GET'])
def recommendLabel():
    caseId = request.args.get('caseId')
    print('caseId',caseId)

    data=getRecommendLabel(caseId)

    return ResponseOK(data)

@app.route('/recommendCode',methods=['GET'])
def recommendCode():
    caseId = request.args.get('caseId')
    print('caseId',caseId)

    data=getRecommendCodes(caseId)

    return ResponseOK(data)

if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    app.run()