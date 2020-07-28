#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import json
import chardet
from src.label_recommand import getRecommendedLabel
from src.code_recommand import getRecommendedCode

import os
def getMd(caseId):
    with open('../cases/'+caseId+'/1/readme.md', 'r', encoding='UTF-8') as f:
        data=f.read()
    print(data)
    return data

def saveCode(caseId,code):
    path='../cases/'+caseId+'/testCode'
    if not os.path.exists(path):
        os.makedirs(path)
    print(path+'/testCode.py')
    with open(path+'/testCode.py','w') as f:
        f.write(code)

    # with open('../cases/'+caseId+'/testCode.py', 'w')as f:
    #     f.write(code)



def getRecommendLabel(caseId):
    path ='../cases/'+caseId+'/recommendLabel.json'
    if not os.path.exists(path):
        getRecommendedLabel(caseId)
    with open(path, 'r')as f:
        res = json.loads(f.read())
    return res

def getRecommendCodes(caseId):
    paths = getRecommendedCode(caseId)
    codes = []
    for path in paths:
        with open(path+'/main.py', 'rb')as f:

            f_read = f.read()
            # 适配编码格式，防止注释中出现中文乱码
            f_charInfo = chardet.detect(f_read)
            # f_charInfo的输出是这样的的一个字典
            # {'confidence': 0.99, 'encoding': 'utf-8'}
            print('编码')
            print(f_charInfo)
            f_read_decode = f_read.decode(f_charInfo['encoding'])
            codes.append(f_read_decode)
    return codes