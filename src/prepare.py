#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import json
import urllib.request, urllib.parse
import string
import zipfile
import shutil
from src.util import *

"""检测代码是不是python。

    Args:
        filePath: 目标代码的文件夹路径

    Returns:
        true：是python
        false：不是python

"""


def checkPython(filePath):
    if filePath.split('/')[-1]=='0':
        if "using namespace std;" in read_file(filePath+'/main.py'):
            return False
        else:
            return True

    path = filePath + '/properties'
    f = open(path, 'r')
    res = f.read()
    data = json.loads(res)
    # print(data)
    if data['lang'] == 'Python3':
        return True
    else:
        return False


"""下载并解压代码.

    Args:
        caseId: 目标题目的ID

    Returns:
        1.返回文件路径数组，格式为caseId/index, 如['../cases/2307/1', '../cases/2307/2', '../cases/2307/3']
        2.储存代码路径数组到filename.json
"""


def downloadAndUnzip(caseId):
    print('-------------下载解压题目--------------------')
    f = open('../data/test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    # print(data)

    filePathList = []
    count = 0

    if not os.path.exists('../cases'):
        os.mkdir('../cases')

    # 创建该case的文件夹
    dir = '../cases/' + caseId
    if not os.path.exists(dir):
        os.mkdir(dir)
    # else:
    #     print('-------------文件已下载--------------------')
    #     return

    for user in data.items():
        cases = user[1]['cases']
        for case in cases:
            if case['case_id'] == caseId:
                if (len(case['upload_records']) == 0):
                    continue

                count += 1
                print(case["case_id"], case["case_type"], count)
                # 获取最后一次提交的url

                url = urllib.parse.quote(case['upload_records'][-1]['code_url'], safe=string.printable)
                url = url.replace(' ', '%20')
                # filenameList.append(os.path.basename(url))
                filename = str(count)

                # filePath = '../cases/' + os.path.basename(url)
                filePath = '../cases/' + caseId + '/' + filename + '.zip'

                urllib.request.urlretrieve(url, filePath)

                # 解压
                f = zipfile.ZipFile(filePath, 'r')
                zipName = f.namelist()[0]
                print('zipName', zipName)
                f.extract(zipName, filePath[:-4] + '/')
                # 二级解压。。
                subFilename = filePath[:-4] + '/' + zipName
                f = zipfile.ZipFile(subFilename, 'r')
                for file in f.namelist():
                    f.extract(file, filePath[:-4] + '/')

                # 过滤非python3答案
                if checkPython(filePath[:-4]):
                    filePathList.append(filePath[:-4])

    # 添加答案代码路径到filePathList
    pathForAnswer = '../cases/' + caseId + '/0'
    if not os.path.exists(pathForAnswer) :
        os.mkdir(pathForAnswer)
        shutil.copy(filePathList[0] + '/.mooctest/answer.py', pathForAnswer + '/main.py')
    if checkPython(pathForAnswer):
        filePathList.append(pathForAnswer)
    # 储存代码路径数组到filename.json

    res = {}
    res[caseId] = filePathList
    print(filePathList)
    orig = getFilePathListAll()
    orig.update(res)
    with open('../data/filename.json', 'w')as f:
        json.dump(orig, f)
    print('-------------下载解压完成--------------------')
    return filePathList


"""获取所有caseId和原题标题.

    Returns:
        1.返回数组，每个item是二元tuple，(caseId, caseName)
"""


def findAllCases():
    f = open('../data/test_data.json', encoding='utf-8')
    data = json.loads(f.read())
    # print(data)

    caseIds = []
    caseNames = []
    count = 0
    for user in data.items():
        cases = user[1]['cases']
        for case in cases:
            if case['case_id'] not in caseIds:
                caseIds.append(case['case_id'])
                caseNames.append(os.path.basename(case['case_zip']).split('_')[0])
    res = list(zip(caseIds, caseNames))
    with open('../data/allCases.json', 'w')as f:
        json.dump(res, f)
    return res


# caseId='2307'
# print(downloadAndUnzip(caseId))
if __name__ == '__main__':
    print(findAllCases())
