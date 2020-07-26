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

    caseId = '2179'

    # downloadAndUnzip(caseId)
    # calcuResults(caseId)
    # rate(caseId)
    searchCase(caseId)
    getRecommendedLabel(caseId)
    # getRecommendedCode(caseId)


