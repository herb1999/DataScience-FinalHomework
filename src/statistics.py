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
            lines = clearCode(f.readlines())
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
    print(results_method)

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
    print('res',res)
    print('-------------CODE 统计完成--------------------')
    return res


"""统计库使用情况 

    Args:
        lines: 代码文本

    Returns:
        res: dict,库名为key，value=1

"""
# todo:找个地方全局sigmoid一下
# todo: as 的检测
def searchLib(lines):#todo:后续要统计库里具体的方法
    res = {'std':sigmoid(1)}
    libs = getLibs()
    for line in lines:
        patterns = re.split(r'\s+', line)
        lib = ''
        # from xxx import xxx 的形式
        if 'from' in line:
            lib = patterns[patterns.index('from') + 1]
        # import xxx 的形式
        else:
            lib = patterns[patterns.index('import') + 1]

        if lib in libs:
            res[lib] = sigmoid(1)


    print('libs found:')
    print(res)
    return res


"""内置方法使用情况

    Args:
        lines: 代码文本
        libs: 代码中使用的库名

    Returns:
        res: dict,方法名为key，value=sigmoid(方法使用次数)

"""
def searchMethod(lines,libs):
    #todo:排除用内置方法名定义的变量和方法
    res = {}
    libsAndMethods = getLibsAndMethods()
    patterns=[]
    for line in lines:
        # 除去注释行
        line = line.strip()
        if line.startswith('#'):
            continue
        patterns.extend(splitLine(line))

    print('patterns found:')
    print(patterns)

    for lib in libs:
        methods= list(libsAndMethods[lib])
        res={ (lib+'.'+method):sigmoid(patterns.count(method))  for method in methods if method in patterns}
    return res


"""根据操作符切分代码

    Args:
        line: 代码行

    Returns:
        切分后的数组

"""
# todo:不要自定义的方法、不要变量
def_list = [] #记录自定义方法名
def_normal=['&','|','~','and','or','elif','if','else','\"']
# 返回使用的库的方法名
# 假设方法名都是在(前面  先以除(外分隔符分割每一行代码
def splitLine(line):
    op = '[=\+\-\*/\[\]\)<>:,]'
    variable = '\s*[a-zA-Z_]+?[\w_]*\s*'
    if(line.strip().startswith("#")):
        return []
    res=(re.split(op,line))
    re_op1 = r'{}\.{}'.format(variable, variable)
    re_op = r'({})'.format(variable, variable)
    re_def=r'def({})'.format(variable)
    list = []
    for item in res:
        cur = re.match(re_def,item)
        if (cur != None):
            def_list.append(cur.group(1).strip())
            continue
        tmp=re.split('\(',item)
        if (len(tmp) <= 1):
            continue
        for i in range(0,len(tmp)-1):
            func = tmp[i].strip()
            if (len(func.split(" ")) > 1)|(len(func)==0):
                continue
            if (func.startswith('.')):
                func = func[1:]
            if(func not in def_list and func not in def_normal):
                list.append(func)
    return list
if __name__ == '__main__':
    # for i in range(0,48):
    #     print("第",i,"道题的方法使用")
    #     with open('../cases/2307/'+str(i)+'/main.py', 'r',encoding='UTF-8') as f:
    #         lines = f.readlines()
    #         for line in lines:
    #             l=splitLine(line)
    #             if(l!=[]):
    #                 print(l)
    searchCase('2307')