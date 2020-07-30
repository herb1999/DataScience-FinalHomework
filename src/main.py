#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from src.prepare import *
from src.rating import *
from src.statistics import *
from src.label_recommand import *
from src.code_recommand import *
# def initAll():
#     findAllCases()
if __name__ == '__main__':
    # 在这里初始化推荐策略，之后可以由网站后端使用
    caseId = '2172'

    # 下载解压
    # downloadAndUnzip(caseId)
    # 运行测试用例，获取代码度量
    # calcuResults(caseId)
    # 代码评分
    rate(caseId)
    # 统计方法/函数
    searchCase(caseId)
    # 计算推荐标签
    getRecommendedLabel(caseId)
