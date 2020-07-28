#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import json
import chardet
from src.label_recommand import getRecommendedLabel
from src.code_recommand import getRecommendedCode

import os

"""获取题目说明

   Args:
       caseId: 题目号
    Returns:
       题目说明md
"""


def getMd(caseId):
    with open('../cases/' + caseId + '/1/readme.md', 'r', encoding='UTF-8') as f:
        data = f.read()
    print(data)
    return data


"""保存新提交的代码

   Args:
       caseId: 新提交的代码对应的题目号
       code:新提交的代码

"""


def saveCode(caseId, code):
    path = '../cases/' + caseId + '/testCode'
    if not os.path.exists(path):
        os.makedirs(path)
    print(path + '/testCode.py')
    with open(path + '/testCode.py', 'w') as f:
        f.write(code)


"""获取推荐标签

   Args:
       caseId: 题号
    Returns:
       推荐标签
"""


def getRecommendLabel(caseId):
    path = '../cases/' + caseId + '/recommendLabel.json'
    if not os.path.exists(path):
        getRecommendedLabel(caseId)
    with open(path, 'r')as f:
        res = json.loads(f.read())
    return res


"""获取推荐代码

   Args:
       caseId: 题号
    Returns:
       推荐代码数组
"""


def getRecommendCodes(caseId):
    paths = getRecommendedCode(caseId)
    codes = []
    for path in paths:
        with open(path + '/main.py', 'rb')as f:
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


"""测试新提交的代码

   Args:
       caseId: 新提交的代码对应的题目号
    Returns:
       通过的测试用例转化的得分
"""


def checkTestCode(caseId):
    bingo = 0
    path = '../cases/' + caseId + '/testCode'
    casePath = '../cases/' + caseId + '/1/.mooctest/testCases.json'
    pyPath = path + '/testCode.py'
    f = open(casePath, 'r')
    res = f.read()
    data = json.loads(res)
    caseNum = len(data)
    for idx, case in enumerate(data):
        inputPath = path + '/input' + str(idx) + '.txt'
        with open(inputPath, 'w')as f:
            f.write(case['input'])
    for idx in range(caseNum):
        inputPath = path + '/input' + str(idx) + '.txt'
        outputPath = path + '/output' + str(idx) + '.txt'
        cmd = 'python' + ' ' + pyPath + ' <' + inputPath + ' >' + outputPath  # py文件的输入输出重定向到input/output文件中
        os.system(cmd)
    for idx in range(caseNum):
        outputPath = path + '/output' + str(idx) + '.txt'
        output = ''
        with open(outputPath, 'r')as f:
            output = f.read()
        if data[idx]['output'] == output:
            bingo += 1
    print(bingo * 100 / caseNum)
    return bingo * 100 / caseNum
