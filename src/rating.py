#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import sys
import json
import urllib.request,urllib.parse
import string
import zipfile
import time
import matplotlib.pyplot as plt
from src.util import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
"""读取目标代码的测试结果的json文件。

    Args:
        filePath: 目标代码的文件夹路径

"""
def checkResult(filePath):
    casePath = filePath + '/result.json'
    f = open(casePath,'r')
    res = f.read()
    data = json.loads(res)
    return data

"""检测代码是不是python。

    Args:
        filePath: 目标代码的文件夹路径
        
    Returns:
        true：是python
        false：不是python

"""
def checkPython(filePath):
    if filePath[-1]=='0':
        return True
    path=filePath+'/properties'
    f = open(path, 'r')
    res = f.read()
    data = json.loads(res)
    # print(data)
    if data['lang']=='Python3':
        return True
    else:
        return False

"""单个case测试,

    Args:
        caseId: 题目ID

    Returns:
        只跑一次，结果存到.mooctest/result.json
        runningTime: 各测试用例运行时间
        runningTimeAvg：测试平均时间
        codeLines：代码行数
        casesResults：测试结果，一个包含0、1的数组，长度为用例数量，用例通过记为1，否则为0
        
"""
def calcuResults(caseId):
    #废案
    #sys.stdin = open('input.txt', 'r')  # 将标准输入重定向为input.txt
    #sys.stdout = open('output.txt', 'w')
    print('-------------测试代码--------------------')
    filePathList=getFilePathList(caseId)

    # 测试用例路径
    casePath = filePathList[1] + '/.mooctest/testCases.json'

    for filePath in filePathList:

        #学生代码路径
        pyPath= filePath +'/main.py'
        f = open(casePath, 'r')
        res = f.read()
        data = json.loads(res)
        caseNum=len(data)
        testRes = {'runningTime': [], 'codeLines': 0, 'casesResults': [],'runningTimeAvg':0}
        #创建用于重定向输入的txt文件
        for idx,case in enumerate(data):
            inputPath=filePath+'/input'+str(idx)+'.txt'
            with open(inputPath,'w')as f:
                f.write(case['input'])

        #以测试用例为输入，运行学生代码，生成测试结果
        runningTime=[]
        for idx in range(caseNum):
            inputPath = filePath + '/input' + str(idx) + '.txt'
            outputPath = filePath + '/output' + str(idx) + '.txt'
            cmd='python'+' '+pyPath+' <'+inputPath+' >'+outputPath # py文件的输入输出重定向到input/output文件中
            start = time.time()
            os.system(cmd)
            end = time.time()
            runningTime.append(end-start)
        testRes['runningTime']=runningTime
        testRes['runningTimeAvg']=np.mean(runningTime)

        #统计测试用例结果
        for idx in range(caseNum):
            outputPath = filePath + '/output' + str(idx) + '.txt'
            output=''
            with open(outputPath, 'r')as f:
                output=f.read()
            if data[idx]['output']==output:
                testRes['casesResults'].append(1)
            else:
                testRes['casesResults'].append(0)

        #统计代码行数
        lineNum=0
        with open(pyPath,'r',encoding='UTF-8') as f:
            lines=f.readlines()
            # for line in lines:
            #     # 除去注释行
            #     realLine = line.lstrip()
            #     if realLine.startswith('#'):
            #         continue
            #     if len(line)>1:
            #         lineNum+=1
            lines=clearCode(lines)
            lineNum=len(lines)
        testRes['codeLines']=lineNum

        resPath = filePath + '/result.json'
        with open(resPath, 'w')as f:
            json.dump(testRes,f)
    print('-------------测试代码完成--------------------')


"""代码评分。

    Args:
        caseId: 题目ID

    Returns:
        评分结果存入data/rated.csv，rate取值区间[0,1]

"""
def rate(caseId):
    print('-------------代码评分--------------------')
    results={'time':[],'lines':[],'path':[]}
    filePathList=getFilePathList(caseId)
    for file in filePathList:
        if checkPython(file):
            # initCase(file)
            data = checkResult(file)
            #排除没有全用例通过的代码
            if 0 in data['casesResults']:
                continue
            results['path'].append(file)
            results['time'].append(data['runningTimeAvg'])
            results['lines'].append(data['codeLines'])
    # print(results)
    df=pd.DataFrame(results)
    # print(df)
    # 0-1标准化
    scaler = MinMaxScaler()
    df['time-std'] = scaler.fit_transform(df['time'].values.reshape(-1, 1))
    df['lines-std'] = scaler.fit_transform(df['lines'].values.reshape(-1, 1))
    # print(df)
    # 评分
    df['rate'] = df[['time-std', 'lines-std']].mean(axis=1)
    print(df)
    # 结果存入data/rated.csv
    print('rate')
    Y=[]
    X=[i for i in range(1,len(df['rate'])+1)]
    for i in range(0,len(df['rate'])):
        Y.append(df['rate'][i])
    Y=sorted(Y)
    plt.plot(X,Y,'ob')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(caseId+'题评分排序')
    plt.ylabel('评分')
    plt.show()
    df.to_csv('../cases/'+caseId+'/rated.csv')
    print('-------------代码评分完成--------------------')

"""代码容量度量。

    Args:
        lines: 代码

    Returns:
        代码容量度量值

"""
def Helstead(lines):
    return 0

if __name__ == '__main__':

    rate('2307')





#

#
# # 错误解决ValueError: Expected 2D array, got 1D array instead:
# # array=[4742.92 3398.   2491.9  2149.   2070.  ].
# # Reshape your data either using array.reshape(-1, 1) if your data has a single feature # # or array.reshape(1, -1) if it contains a single sample.
#
# ### 使用array.reshape(-1, 1)重新调整你的数据）python3 加values
#


