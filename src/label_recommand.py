#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import sys
import json
import re

from matplotlib.ticker import MultipleLocator

from src.util import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f
from scipy.cluster.vq import vq, kmeans, whiten
from sklearn.decomposition import PCA
import prettytable as pt

"""对簇和评分的关系进行方差分析

    args:
        clusters: 聚类得到的DataFrame数组
        
"""
def F_test(clusters):
    print('----------方差分析------------')
    k=len(clusters)
    rates = []
    mean_list = []
    var_list = []
    num_list = []
    num_total = 0
    mean_total = 0
    for cluster in clusters:
        rates.append(list(cluster['rate']))
    # print(rates)
    # 求各组均值\方差\个数
    for rate in rates:
        mean_list.append(np.mean(rate))
        var_list.append(np.var(rate))
        num_list.append(len(rate))

    # 求总体均值、个数
    num_total = sum(num_list)
    mean_total = sum(map(lambda x: x[0] * x[1], zip(mean_list, num_list))) / num_total

    # 总偏差平方和 SS
    SS = 0
    for rate in rates:
        rate = np.array(rate)
        SS += np.sum((rate - mean_total) ** 2)

    # 组内偏差 SSe
    SSe = 0
    for idx, rate in enumerate(rates):
        rate = np.array(rate)
        SSe += np.sum((rate - mean_list[idx]) ** 2)

    # 组间偏差 SSa
    SSa = SS - SSe
    # 组件偏差验证
    SSaTest = 0
    for idx, mean in enumerate(mean_list):
        SSaTest += (mean - mean_total) ** 2 * num_list[idx]

    # 自由度
    df=num_total-1
    dfa=k-1
    dfe=num_total-k

    MSa=SSa/dfa
    MSe=SSe/dfe

    F=MSa/MSe
    p=f.sf(F,dfa,dfe)
    print(mean_list)
    print(var_list)
    print(num_list)
    print(num_total)
    print(mean_total)

    table = pt.PrettyTable(['项目','平方和 ','自由度 ','均方和 ','F比值 ','p值 '])
    table.add_row(['簇的差异',format(SSa, '.4f'),dfa,format(MSa, '.4f'),format(F, '.4f'),format(p, '.4f')])
    table.add_row(['误差', format(SSe, '.4f'), dfe, format(MSe, '.4f'), '-', '-'])
    table.add_row(['总和', format(SS, '.4f'), df, '-', '-', '-'])
    print(table)
    print('----------方差分析完毕------------')

"""绘制聚类结果.

    Args:
        X: 代码的方法/函数统计数据
        label：聚类得到的分类标签
        k：簇的个数

"""
def draw_after_kmeans(X, label, k):
    idx = []  # 分类结果，为X中的行下标
    clusters = []  # 使用下标分开的dataFrames
    for i in range(k):
        idx.append(np.where(label == i)[0])
        clusters.append(X[idx[i], :])
    fig, ax = plt.subplots(figsize=(9, 6))
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    for i in range(k):
        ax.scatter(clusters[i][:, 0], clusters[i][:, 1], s=30, color=colors[i], label='Cluster ' + str(i + 1))
    ax.legend()
    plt.show()

"""绘制簇和对应代码评分.

    Args:
        X: 代码的方法/函数统计数据
        label：聚类得到的分类标签
        k：簇的个数

"""
def draw_label_and_rate(X, label, k):
    fig, ax = plt.subplots(figsize=(9, 6))
    for i in range(k):
        ax.scatter(label, X['rate'], s=30, color='c', label='Cluster ' + str(i + 1))
    x_major_locator = MultipleLocator(1)
    ax.xaxis.set_major_locator(x_major_locator)  # x轴按1刻度显示
    plt.xlabel('Cluster')
    plt.ylabel('rate')
    plt.show()

"""肘部法则优化k值.

    Args:
        X: 代码的方法/函数统计数据
        label：聚类得到的分类标签
        k：簇的个数
        
    Returns：
        最佳k值

"""
def find_best_k(lossList, minK,caseId):
    manual_k={'2908':7}
    if caseId in manual_k:
        return manual_k[caseId]
    maxK = minK + len(lossList)
    kList = range(minK, maxK)
    plt.xlabel('k')
    plt.ylabel('Cost')

    plt.plot(kList, lossList,'-o')
    plt.show()

    cosVals = []
    for i in range(1, len(lossList) - 1):
        v1 = [1, lossList[i] - lossList[i - 1]]
        v2 = [1, lossList[i + 1] - lossList[i]]
        cosVals.append(cosine_similarity(v1, v2))

    plt.xlabel('k')
    plt.ylabel('cos')
    x_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)  # x轴按1刻度显示
    plt.plot(kList[1:-1], cosVals,'-o')
    plt.show()
    idx = int(np.argmin(cosVals)) + 1
    print(idx)
    return kList[idx]


"""获取推荐标签

    Args:
        caseId: 题目ID

    Returns:
        labels,标签
        bestCodePaths,聚类分开的dataFrames中评分最高的code的path

"""



# todo: 或者探索一下方法与评分的关联性？
def getRecommendedLabel(caseId):
    print('-------------标签推荐开始--------------------')
    # stat = getStatistics(caseId)
    # sums = stat.iloc[:, 1:].sum().sort_values(ascending=False)
    # # stat.sort_values()
    # print(sums)
    # print('-------------标签推荐完成--------------------')
    # return sums[:4]

    minK = 2
    maxK = 7

    stat = getStatistics(caseId).set_index('path').fillna(0)
    rated = getRated(caseId)
    rated = pd.DataFrame(rated, columns=['path', 'rate'])
    print(rated)
    X = pd \
        .merge(stat, rated, on='path', how='outer') \
        .fillna(0) \
        .set_index('path')
    print(X)
    # 降维部分
    pca = PCA(n_components=2)
    pca.fit(stat)
    print(pca.explained_variance_ratio_)
    X_new = pca.transform(stat)
    print(X_new)
    plt.scatter(X_new[:, 0], X_new[:, 1], marker='o')
    plt.show()

    # pca = PCA(n_components='mle')
    # pca.fit(X)
    # print(pca.explained_variance_ratio_)
    # X_new = pca.transform(X)
    # print(X_new)


    # 聚类部分
    centroidsList = []
    lossList = []
    for k in range(minK, maxK + 1):
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html#scipy.cluster.vq.kmeans
        centriods, loss = kmeans(X_new, k_or_guess=k,iter=300)
        lossList.append(loss)
        centroidsList.append(centriods)

    # 肘部优化法确定最佳K值
    bestK = find_best_k(lossList, minK , caseId)
    print("bestK:  " + str(bestK))
    bestCentroids = centroidsList[bestK - minK]

    label = vq(X_new, bestCentroids)[0]
    print(label)
    idx = []  # 分类结果，为X中的行下标
    clusters = []  # 使用下标分开的dataFrames
    rate = []  # 各cluster的平均评分
    for i in range(bestK):
        idx.append(np.where(label == i)[0])
        clusters.append(X.iloc[idx[i], :])
        rate.append(np.sum(clusters[i]['rate']) / len(idx[i]))
    # print(X[np.where(label == 0)[0], :])
    # print(X)
    # print(clusters[0])
    # print(rate)
    # print(np.argmin(rate))
    # print(clusters[int(np.argmin(rate))])

    draw_after_kmeans(X_new, label, bestK)
    draw_label_and_rate(X, label, bestK)
    # F_test(clusters)

    labels = clusters[int(np.argmin(rate))].drop('rate', axis=1).sum().sort_values(ascending=False)
    # stat.sort_values()
    print(labels)
    # 保存推荐结果
    with open('../cases/' + caseId + '/recommendLabel.json', 'w')as f:
        json.dump(dict(labels), f)

    # 获取各个簇中评分最高的代码路径
    bestCodePaths = []
    for cluster in clusters:
        # print('cluster')
        # print(cluster)
        # dataFrame以path为idx，argmax直接得到path
        bestCodePaths.append(np.argmin(cluster['rate']))
    print('bestCodePaths: ')
    print(bestCodePaths)
    # 保存代码路径
    with open('../cases/' + caseId + '/bestCodes.json', 'w')as f:
        json.dump(bestCodePaths, f)
    print('-------------标签推荐完成--------------------')
    return labels, bestCodePaths


#
# def init_centroids(X, k):
#     m, n = X.shape
#     centroids = np.zeros((k, n))
#     idx = np.random.randint(0, m, k)
#
#     for i in range(k):
#         centroids[i, :] = X[idx[i], :]
#
#     return centroids
#
#
# def find_closest_centroids(X, centroids):
#     m = X.shape[0]
#     k = centroids.shape[0]
#     idx = np.zeros(m)
#
#     for i in range(m):
#         min_dist = 1000000
#         for j in range(k):
#             dist = np.sum((X[i, :] - centroids[j, :]) ** 2)
#             if dist < min_dist:
#                 min_dist = dist
#                 idx[i] = j
#
#     return idx
#
#
# def compute_centroids(X, idx, k):
#     m, n = X.shape
#     centroids = np.zeros((k, n))
#
#     for i in range(k):
#         indices = np.where(idx == i)  # 找出idx中值为i的数的下标
#         centroids[i, :] = (np.sum(X[indices, :], axis=1) / len(indices[0])).ravel()
#     return centroids
#
#
# def k_means(X, k, max_iters):
#     m, n = X.shape
#     X = X.values  # X转ndarray，不然报错
#     idx = np.zeros(m)
#     centroids = init_centroids(X, k)
#
#     for i in range(max_iters):
#         idx = find_closest_centroids(X, centroids)
#         centroids = compute_centroids(X, idx, k)
#     return idx, centroids


"""
测试代码
"""
if __name__ == '__main__':
    getRecommendedLabel('2908')
# stat = getStatistics('2307')
# rated = getRated('2307')
# X =pd\
#         .merge(stat, rated, on='path',how='outer')\
#         .fillna(0)\
#         .set_index('path')
# print(X)
# testData = pd.DataFrame(X, columns=['input', 'list'])
# print(testData)
# # https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html#scipy.cluster.vq.kmeans
# testData = testData.values
# X=X.values
# centriods = kmeans(X, k_or_guess=3)[0]
# label = vq(X, centriods)[0]
# print(label)
# idx1=np.where(label == 0)[0]
# idx2=np.where(label == 1)[0]
# idx3=np.where(label == 2)[0]
# cluster1 = testData[idx1, :]
# cluster2 = testData[idx2, :]
# cluster3 = testData[idx3, :]
# # print(X[np.where(label == 0)[0], :])
#
# rate1 = np.sum(X[idx1, -1])/len(idx1)
# rate2 = np.sum(X[idx2, -1])/len(idx2)
# rate3 = np.sum(X[idx3, -1])/len(idx3)
# print([rate1,rate2,rate3])
# print(np.where(label == 0))
# print(len(np.where(label == 0)[0]))
# cluster4 = centriods
# fig, ax = plt.subplots(figsize=(9, 6))
# ax.scatter(cluster1[:, 0], cluster1[:, 1], s=30, color='r', label='Cluster 1')
# ax.scatter(cluster2[:, 0], cluster2[:, 1], s=30, color='g', label='Cluster 2')
# ax.scatter(cluster3[:, 0], cluster3[:, 1], s=30, color='b', label='Cluster 3')
# ax.scatter(cluster4[:, 0], cluster4[:, 1], s=30, color='c', label='centriods')
# ax.legend()
# plt.show()
