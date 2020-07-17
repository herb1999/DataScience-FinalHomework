#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import re
#
# a=np.mat([[1.1,2,3],[4,5,6],[12,45,-60]])
# def norm(mat):
#     m=mat.shape[0]
#     n=mat.shape[1]
#     for i in range(m):
#         arr=mat[i,:]
#         mean = np.sum(arr)/n
#         var=np.sum(np.multiply((arr-mean),(arr-mean)))/n
#         arrNorm=(arr-mean)/np.sqrt(var+1e-8)
#         mat[i]=arrNorm
#     return mat
# print(norm(a))

# a='1+2-3=4-ans(as)'
# print(re.split(r'[+\-=*/()\[\]{\}]+',a))

a={1:2}
a=pd.Series(a)
b={3:4}
b=pd.Series(b)
print(pd.concat([a,b]))
c=pd.DataFrame([1,2])
print(c)
print(c.shape)
