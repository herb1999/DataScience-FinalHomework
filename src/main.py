#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from src.prepare import *
from src.rating import *
from src.statistics import *
from src.label_recommand import *
from src.code_recommand import *
if __name__ == '__main__':
    # todo:记一下哪个例子比较好用
    # 2908  F 8.5
    # 2804  F 10
    # 2456  F 6.3  0.002

    # 推荐代码 2176/63、34
    # 面向用例 2176/1
    caseId = '2172'

    # downloadAndUnzip(caseId)
    # calcuResults(caseId)
    # rate(caseId)
    searchCase(caseId)
    getRecommendedLabel(caseId)

