#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import sys
import json
import re
from src.util import *
from src.statistics import *
import pandas as pd
import numpy as np


"""获取推荐代码

    Args:
        path: 新提交的代码路径
        caseId: 题目ID

    Returns:
        距离最近和最远的代码

"""
# todo:pearson：Pearson\kendall\spearman相关系数? 有没有比余弦距离更好的度量两个向量的相关性的方法？
def getRecommendedCode(path,caseId):
    print('-------------代码推荐开始--------------------')
    stat=getStatistics(caseId)
    newStat=searchCode(path)
    newStat['path']=path
    # print(newStat)
    # print(stat)
    stat=stat.append(newStat,ignore_index=True).fillna(0) #把新代码的统计量合并到dataFrame里，用来保证所有的代码的统计量长度一致
    # print(stat)
    # print(stat.shape)
    v1=list(stat.iloc[-1,1:])
    cor=[]
    for i in range(stat.shape[0]-1):
        v2=list(stat.iloc[i,1:])
        cor.append(cosine_similarity(v1,v2))
    cor.append(1)
    # print(cor)
    stat['cor']=cor
    stat=stat.sort_values(by='cor',ascending=False)
    print(stat)
    # print(list(stat.iloc[1,:]))
    print('最相似 : '+stat.iloc[1]['path'])
    print('最不相似 : ' + stat.iloc[-1]['path'])
    print('-------------代码推荐完成--------------------')
    return







# getRecommendedCode('../cases/2307/4','2307')