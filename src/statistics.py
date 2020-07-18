#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import sys
import json
import re
from src.util import *
import pandas as pd
import numpy as np
from math import cos

# todo:内置类的方法统计
"""统计case中所有代码的库、方法、语法糖。

    Args:
        caseId: 题目ID

    Returns:
        得到以代码路径为索引，统计对象为列标签的dataFrame，结果保存到'../cases/' + caseId + '/statistics.csv'
        
"""
def searchCase(caseId):

    print('-------------CASE 统计开始--------------------')
    rated = getRated(caseId)
    paths = list(rated.sort_values(by='rate')['path'])
    print(paths)

    # libs = getLibs()
    # print(libs)


    results_lib = []
    results_method = []
    results_candy = []
    for path in paths:
        with open(path+'/main.py', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            res=searchLib(lines)
            if len(res)>0:
                res['path']=path
                results_lib.append(res)

            res=searchMethod(lines)
            if len(res)>0:
                res['path'] = path
                results_method.append(res)
    #库统计结果
    results_lib=pd.DataFrame(results_lib)
    # 内置方法统计结果
    results_method=pd.DataFrame(results_method)
    # print('results_lib: ')
    print(results_lib)
    # print('results_method: ')
    # print(results_method)

    # 统计结果合并
    df=pd\
        .merge(results_lib, results_method, on='path',how='outer')\
        .fillna(0)\
        .set_index('path')
    print(df)
    df.to_csv('../cases/' + caseId + '/statistics.csv')
    print('-------------CASE 统计完成--------------------')


"""统计单个代码中的库、方法、语法糖。

    Args:
        path: 代码路径

    Returns:
        统计对象为列标签，使用次数为值的Series

"""
def searchCode(path):
    print('-------------CODE 统计开始--------------------')
    results_lib = []
    results_method = []
    results_candy = []
    with open(path+'/main.py', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        res = searchLib(lines)
        results_lib=pd.Series(res)

        res = searchMethod(lines)
        results_method=pd.Series(res)

    print(results_lib)
    print(results_method)
    # 统计结果合并
    res = pd.concat([results_method,results_lib])
    print(res)
    print('-------------CODE 统计完成--------------------')
    return res


"""统计库使用情况 

    Args:
        lines: 代码文本

    Returns:
        res: dict,库名为key，value=1

"""
def searchLib(lines):#todo:后续要统计库里具体的方法
    res = {}
    for line in lines:
        # 除去注释行
        line = line.strip()
        if line.startswith('#'):
            continue
        if 'import' in line:
            print('found: ' + line)
            patterns = line.split(' ')

            # from xxx import xxx 的形式
            if 'from' in line:
                lib = patterns[patterns.index('from') + 1]
                res[lib] = sigmoid(1)
            # import xxx 的形式
            else:
                lib = patterns[patterns.index('import') + 1]
                res[lib] = sigmoid(1)
    return res


"""内置方法使用情况

    Args:
        lines: 代码文本

    Returns:
        res: dict,方法名为key，value=sigmoid(方法使用次数)

"""
def searchMethod(lines):
    #todo:排除用内置方法名定义的变量和方法
    res = {}
    methods = getBuiltinMethods()
    patterns=[]
    for line in lines:
        # 除去注释行
        line = line.strip()
        if line.startswith('#'):
            continue
        patterns.extend(splitLine(line))

    res={ method:sigmoid(patterns.count(method))  for method in methods if method in patterns}
    return res


"""根据操作符切分代码

    Args:
        line: 代码行

    Returns:
        切分后的数组

"""
def splitLine(line):
    #操作符有的要转义，有的不用，测试清楚
    op = '[=\+\-\*/\[\]\(\)]'
    variable = '\s*[a-zA-Z_]+?[\w_]*\s*'
    #先以操作符分割字符串
    res = (re.split(op, line))
    re_op1 = r'{}\.{}'.format(variable, variable)
    re_op = r'({})'.format(variable, variable)
    list = []
    #得到变量名/函数名
    for item in res:
        if (re.match(re_op1, item) != None):
            list.append(item)
        else:
            if (re.match(re_op, item) != None):
                list.append(re.match(re_op, item).group(0))
    # print(list)
    return list

if __name__ == '__main__':
    with open('../cases/2307/32/main.py','r') as f:
        lines=f.readlines()
        for line in lines:
            print(splitLine(line))