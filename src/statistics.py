#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import sys
import json
import re
from src.util import *
import pandas as pd
import numpy as np


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
        with open(path + '/main.py', 'r', encoding='UTF-8') as f:
            lines = clearCode(f.readlines())
            libs, asMethodMap = searchLib(lines)  # 获取库
            results_lib.extend(libs)
            res = searchMethod(lines, libs)  # 获取方法
            # if len(res)>0:
            res['path'] = path
            results_method.append(res)
    # 库统计结果

    # 方法统计结果
    results_method = pd.DataFrame(results_method)
    paths = results_method.path
    results_method = results_method.drop('path', axis=1)
    results_method.insert(0, 'path', paths)
    results_method.set_index('path')
    results_method = results_method.fillna(0)
    print('results_lib: ')
    print(results_lib)
    print('results_method: ')
    print(list(results_method))
    print(results_method.fillna(0))

    results_method.to_csv('../cases/' + caseId + '/statistics.csv')
    print('-------------CASE 统计完成--------------------')


"""统计单个代码中的函数、方法。

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
    with open(path, 'r', encoding='unicode_escape') as f:
        lines = f.readlines()
        results_lib, asMap = searchLib(lines)
        res = searchMethod(lines, results_lib)
        results_method = pd.Series(res)

    print(results_method)
    print('-------------CODE 统计完成--------------------')
    return results_method


"""统计库使用情况 

    Args:
        lines: 代码文本

    Returns:
        res: 检测到的库名，list
        asMethodMap: 用as引入的方法名，dict，key=新名  value=原名

"""



def searchLib(lines):
    res = ['std', 'list', 'dict', 'str', 'set']
    asLibMap = {}  # 新名：原名
    asMethodMap = {}  # 新名：原名
    libs = getLibs()
    for line in lines:
        patterns = re.split(r'\s+', line)
        lib = ''
        # from xxx import xxx 的形式
        if 'from' in patterns:
            lib = patterns[patterns.index('from') + 1]
            if 'as' in patterns:
                func = patterns[patterns.index('import') + 1]
                asMethodMap.update({patterns[patterns.index('as') + 1]: lib + "." + func})
        # import xxx 的形式
        elif 'import' in patterns:
            lib = patterns[patterns.index('import') + 1]
            # if 'as' in patterns:
            #     asLibMap.update({lib: patterns[patterns.index('as') + 1]})
        else:
            continue
        print(lib)
        if lib in libs and len(lib) > 0:
            res.append(lib)
    print('libs found:')
    print(res)
    print('asMethodMap')
    print(asMethodMap)
    return res, asMethodMap


"""方法使用情况

    Args:
        lines: 代码文本
        libs: 代码中使用的库名

    Returns:
        res: dict,方法名为key，value=sigmoid(方法使用次数)

"""
def searchMethod(lines, libs):
    res = {}
    libsAndMethods = getLibsAndMethods()
    patterns = []
    for line in lines:
        # 除去注释行
        line = line.strip()
        if line.startswith('#'):
            continue
        patterns.extend(splitLine(line))

    print('patterns found:')
    print(patterns)
    patterns=list(map(lambda s:s.split('.')[-1],patterns))
    for lib in libs:
        methods = list(libsAndMethods[lib])
        for method in methods:
            if method in patterns:
                res[(lib + '.' + method)] = sigmoid(patterns.count(method))

    return res


"""根据操作符切分代码

    Args:
        line: 代码行

    Returns:
        切分后的数组

"""

def_list = []  # 记录自定义方法名
def_normal = ['&', '|', '~', 'and', 'or', 'elif', 'if', 'else', '\"']


# 返回使用的库的方法名
# 假设方法名都是在(前面  先以除(外分隔符分割每一行代码
def splitLine(line):
    op = '[=\+\-\*/\[\]\)<>:,]'
    variable = '\s*[a-zA-Z_]+?[\w_]*\s*'
    if (line.strip().startswith("#")):
        return []
    res = (re.split(op, line))
    re_op1 = r'{}\.{}'.format(variable, variable)
    re_op = r'({})'.format(variable, variable)
    re_def = r'def({})'.format(variable)
    list = []
    for item in res:
        cur = re.match(re_def, item)
        if (cur != None):
            def_list.append(cur.group(1).strip())
            continue
        tmp = re.split('\(', item)
        if (len(tmp) <= 1):
            continue
        for i in range(0, len(tmp) - 1):
            func = tmp[i].strip()
            if (len(func.split(" ")) > 1) | (len(func) == 0):
                continue
            if (func.startswith('.')):
                func = func[1:]
            if (func not in def_list and func not in def_normal):
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
    searchCase('2179')
    # with open('../cases/2307/24/main.py','r',encoding='UTF-8') as f:
    # with open('../cases/try.py', 'r', encoding='UTF-8') as f:
    #     lines = f.readlines()
    #     print(searchLib(lines))
