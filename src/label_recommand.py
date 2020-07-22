#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import sys
import json
import re
from src.util import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from scipy.io import loadmat
import sklearn
from scipy.cluster.vq import vq, kmeans, whiten
from sklearn.decomposition import PCA

def draw_after_kmeans(X,label,k):
    idx = []  # 分类结果，为X中的行下标
    clusters = []  # 使用下标分开的dataFrames
    for i in range(k):
        idx.append(np.where(label == i)[0])
        clusters.append(X[idx[i], :])
    fig, ax = plt.subplots(figsize=(9, 6))
    colors=['r','g','b','c']
    for i in range(k):
        ax.scatter(clusters[i][:, 0], clusters[i][:, 1], s=30, color=colors[i], label='Cluster '+str(i+1))
    ax.legend()
    plt.show()

"""获取推荐标签

    Args:
        caseId: 题目ID

    Returns:
        使用量靠前的标签

"""


# todo:k值优化
# todo:可能漏掉使用少但是关键的label
# todo: 难点：证明label聚出的类和评分的相关性，这样才可以对所有代码聚类，选出评分最高的一个类；不然就只能评分选代码，再聚类
# todo: 或者探索一下方法与评分的关联性？
def getRecommendedLabel(caseId):
    print('-------------标签推荐开始--------------------')
    # stat = getStatistics(caseId)
    # sums = stat.iloc[:, 1:].sum().sort_values(ascending=False)
    # # stat.sort_values()
    # print(sums)
    # print('-------------标签推荐完成--------------------')
    # return sums[:4]

    k = 4

    stat = getStatistics(caseId)
    rated = getRated(caseId)
    rated = pd.DataFrame(rated, columns=['path', 'rate'])  # todo:是把评分用到的度量特征和方法使用放在一起聚类，还是只用方法？
    print(rated)
    X = pd \
        .merge(stat, rated, on='path', how='outer') \
        .fillna(0) \
        .set_index('path')
    print(X)
    # 降维部分
    pca = PCA(n_components=2)
    pca.fit(X)
    X_new = pca.transform(X)
    print(X_new)
    plt.scatter(X_new[:, 0], X_new[:, 1], marker='o')
    plt.show()

    # 聚类部分
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html#scipy.cluster.vq.kmeans
    centriods, loss = kmeans(X_new, k_or_guess=k)  # todo:之后根据loss优化k值
    label = vq(X_new, centriods)[0]
    print(label)
    idx = []  # 分类结果，为X中的行下标
    clusters = []  # 使用下标分开的dataFrames
    rate = []  # 各cluster的平均评分
    for i in range(k):
        idx.append(np.where(label == i)[0])
        clusters.append(X.iloc[idx[i], :])
        rate.append(np.sum(clusters[i]['rate']) / len(idx[i]))
    # print(X[np.where(label == 0)[0], :])
    print(X)
    print(clusters[0])
    print(rate)
    print(np.argmin(rate))
    print(clusters[int(np.argmin(rate))])
    draw_after_kmeans(X_new,label,k)
    sums = clusters[int(np.argmin(rate))].drop('rate',axis=1).sum().sort_values(ascending=False)
    # stat.sort_values()
    print(sums)
    print('-------------标签推荐完成--------------------')
    return sums[:4]


# 目的：值得推荐的代码可能有十几个，也可能只有几个，要靠聚类区分出最优秀的一类代码


def init_centroids(X, k):
    m, n = X.shape
    centroids = np.zeros((k, n))
    idx = np.random.randint(0, m, k)

    for i in range(k):
        centroids[i, :] = X[idx[i], :]

    return centroids


def find_closest_centroids(X, centroids):
    m = X.shape[0]
    k = centroids.shape[0]
    idx = np.zeros(m)

    for i in range(m):
        min_dist = 1000000
        for j in range(k):
            dist = np.sum((X[i, :] - centroids[j, :]) ** 2)
            if dist < min_dist:
                min_dist = dist
                idx[i] = j

    return idx


def compute_centroids(X, idx, k):
    m, n = X.shape
    centroids = np.zeros((k, n))

    for i in range(k):
        indices = np.where(idx == i)  # 找出idx中值为i的数的下标
        centroids[i, :] = (np.sum(X[indices, :], axis=1) / len(indices[0])).ravel()
    return centroids


def k_means(X, k, max_iters):
    m, n = X.shape
    X = X.values  # X转ndarray，不然报错
    idx = np.zeros(m)
    centroids = init_centroids(X, k)

    for i in range(max_iters):
        idx = find_closest_centroids(X, centroids)
        centroids = compute_centroids(X, idx, k)
    return idx, centroids


"""
测试代码
"""
if __name__ == '__main__':
    getRecommendedLabel('2307')
    print(dir())
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
