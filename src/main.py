#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from src.prepare import *
from src.rating import *
from src.statistics import *
from src.label_recommand import *
from src.code_recommand import *
if __name__ == '__main__':
    caseId = '2307'

    downloadAndUnzip(caseId)
    calcuResults(caseId)
    rate(caseId)
    searchCase(caseId)
    getRecommendedLabel(caseId)
    # getRecommendedCode(caseId)


