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
        newPath: 新提交的代码路径
        caseId: 题目ID

    Returns:
        推荐代码的path列表，包括标准答案，以及聚类后的各个簇中评分最高的，按照相似度排序

"""
# todo:pearson：Pearson\kendall\spearman相关系数? 有没有比余弦距离更好的度量两个向量的相关性的方法？
def getRecommendedCode(caseId):
    print('-------------代码推荐开始--------------------')
    allPaths=[]

    # 获取聚类后的各个簇中评分最高的代码的路径
    with open('../cases/' + caseId + '/bestCodes.json', 'r')as f:
        res = f.read()
        data = json.loads(res)
        # data = map(lambda p:p+'/main.py',data)
    allPaths.extend(data)

    # 添加标准答案路径
    # allPaths.append('../cases/'+caseId+'/0/main.py')
    allPaths.append('../cases/' + caseId + '/0')

    # 添加新提交的代码的路径
    newPath='../cases/' + caseId +'/testCode'+ '/testCode.py'
    # allPaths.append(newPath)

    # 去重
    allPaths=list(set(allPaths))

    stat_=getStatistics(caseId)
    stat=pd.DataFrame()
    for path in allPaths:
        idx=np.where(stat_['path']==path)
        stat=stat.append(stat_.iloc[idx[0]],ignore_index=True)
    print(stat)
    newStat=searchCode(newPath)
    newStat['path']=newPath
    # print(newStat)
    # print(stat)
    stat=stat.append(newStat,ignore_index=True).fillna(0) #把新代码的统计量合并到dataFrame里，用来保证所有的代码的统计量长度一致
    print(stat)
    # print(stat.shape)
    v1=list(stat.iloc[-1,1:])
    cor=[]
    for i in range(stat.shape[0]-1):
        v2=list(stat.iloc[i,1:])
        print(v1)
        print(v2)
        cor.append(cosine_similarity(v1,v2))
    cor.append(1)
    # print(cor)
    stat['cor']=cor
    stat=stat.iloc[:-1].sort_values(by='cor',ascending=False)
    print(stat)
    # print(list(stat.iloc[1,:]))
    print('最相似 : '+stat.iloc[0]['path'])
    print('最不相似 : ' + stat.iloc[-1]['path'])
    print('-------------代码推荐完成--------------------')
    return stat['path']






if __name__ == '__main__':

    getRecommendedCode('2908')