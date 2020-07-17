#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from src.prepare import *
from src.rating import *
from src.statistics import *
from src.label_recommand import *
from src.code_recommand import *
caseId='2307'

downloadAndUnzip(caseId)
calcuResults(caseId)
rate(caseId)
searchCase(caseId)
getRecommendedLabel(caseId)
getRecommendedCode('../cases/2307/4','2307')


