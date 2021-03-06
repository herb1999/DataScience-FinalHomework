#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import sys
import json
import urllib.request,urllib.parse
import string
import zipfile
import time

import chardet
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def read_file(path):
    with open(path, 'rb')as f:
        f_read = f.read()
        # 适配编码格式，防止注释中出现中文乱码
        f_charInfo = chardet.detect(f_read)
        # f_charInfo的输出是这样的的一个字典
        # {'confidence': 0.99, 'encoding': 'utf-8'}
        print('编码')
        print(f_charInfo)
        f_read_decode = f_read.decode(f_charInfo['encoding'])
        return f_read_decode
def cosine_similarity(x, y, norm=False):
    """ 计算两个向量x和y的余弦相似度 """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)

    # method 1
    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

    # method 2
    # cos = bit_product_sum(x, y) / (np.sqrt(bit_product_sum(x, x)) * np.sqrt(bit_product_sum(y, y)))

    # method 3
    # dot_product, square_sum_x, square_sum_y = 0, 0, 0
    # for i in range(len(x)):
    #     dot_product += x[i] * y[i]
    #     square_sum_x += x[i] * x[i]
    #     square_sum_y += y[i] * y[i]
    # cos = dot_product / (np.sqrt(square_sum_x) * np.sqrt(square_sum_y))

    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内
def getFilePathList(caseId):
    with open('../data/filename.json', 'r')as f:
        res = f.read()
        data = json.loads(res)
        filePathList=data[caseId]
    return filePathList

def getFilePathListAll():
    with open('../data/filename.json', 'r')as f:
        res = f.read()
        data = json.loads(res)
    return data

def getAllCases():
    allCases = []
    with open('../data/allCases.json', 'r')as f:
        res = f.read()
        allCases = json.loads(res)
    return allCases

def getRated(caseId):
    return pd.read_csv('../cases/'+caseId+'/rated.csv').iloc[:,1:]

def getLibs():
    return list(pd.read_csv('../data/libs.csv').columns.values)

def getLibsAndMethods():
    return pd.read_csv('../data/libs.csv')

def getStatistics(caseId):
    return pd.read_csv('../cases/' + caseId + '/statistics.csv').iloc[:,1:]

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def getRecommendCodePaths(caseId):
    with open('../cases/' + caseId + '/recommendCode.json', 'r')as f:
        res = f.read()
        data = json.loads(res)
    return data
"""过滤空行、注释，包括单行、多行注释、跟着代码的行后注释

Args:
    lines: 学生代码，string数组

Returns:
    过滤后的代码

"""
def clearCode(lines):
    rows = False
    res = []
    for line in lines:
        #处理掉 ;
        line=line.replace(';','')
        if line.strip()=='':
            continue
        if (rows):
            if (line.find("'''") != -1):
                rows = False
        else:
            idx = line.find("'''")
            if idx != -1:
                rows = True
                continue
            idx = line.find('#')
            if idx != -1:
                if idx == 0:
                    continue
                line = line[0:idx]
            if line.strip() == '':
                continue
            res.append(line)
    return res


if __name__ == '__main__':
    # print(getLibs())
    # print(getStatistics('2307'))
    # print(getRated('2307'))
    print(getAllCases())
    with open('../cases/2307/24/main.py', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        print(clearCode(lines))



# X=[]
# Y=[]
# for file in filenameList:
#     if checkPython(file):
#         # initCase(file)
#         data=checkResult(file)
#         if 0 in data['casesResults']:
#             continue
#         X.append(data['codeLines'])
#         Y.append(data['runningTimeAvg'])

# plt.figure()
# plt.title('2307题分析')
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus']=False
# ax = plt.gca()
# # ax.spines['bottom'].set_position(('data',0))
# # ax.spines['left'].set_position(('data',0))
# ax.spines['top'].set_color('none')
# ax.spines['right'].set_color('none')
# plt.scatter(X,Y,s=20)
# plt.xlabel('代码行数')
# plt.ylabel('运行时间')
# plt.show()
#
