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
# todo:pearson：Pearson\kendall\spearman相关系数?
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




def cosine_similarity(x, y, norm=False):
    """ 计算两个向量x和y的余弦相似度 """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)

    # method 1
    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

    # method 2
    # cos = bit_product_sum(x, y) / (np.sqrt(bit_product_sum(x, x)) * np.sqrt(bit_product_sum(y, y)))

    # method 3
    # dot_product, square_sum_x, square_sum_y = 0, 0, 0
    # for i in range(len(x)):
    #     dot_product += x[i] * y[i]
    #     square_sum_x += x[i] * x[i]
    #     square_sum_y += y[i] * y[i]
    # cos = dot_product / (np.sqrt(square_sum_x) * np.sqrt(square_sum_y))

    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内


# getRecommendedCode('../cases/2307/4','2307')