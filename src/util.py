#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import sys
import json
import urllib.request,urllib.parse
import string
import zipfile
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def getFilePathList(caseId):
    filePathList=[]
    with open('../data/filename.json', 'r')as f:
        res = f.read()
        data = json.loads(res)
        filePathList=data[caseId]
    return filePathList

def getRated(caseId):
    return pd.read_csv('../cases/'+caseId+'/rated.csv')

def getLibs():
    return list(pd.read_csv('../data/libs.csv').columns.values)

def getLibsAndMethods():
    return list(pd.read_csv('../data/libs.csv'))

def getStatistics(caseId):
    return pd.read_csv('../cases/' + caseId + '/statistics.csv')

def sigmoid(x):
    return 1/(1 + np.exp(-x))

#todo 过滤空行、注释，包括单行、多行注释、跟着代码的行后注释
def clearCode(lines):
    return lines


if __name__ == '__main__':
    print(getLibs())


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
