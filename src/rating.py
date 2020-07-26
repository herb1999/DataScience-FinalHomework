#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from collections import Counter
from src.util import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from math import log2
import re
"""读取目标代码的测试结果的json文件。

    Args:
        filePath: 目标代码的文件夹路径

"""
def checkResult(filePath):
    casePath = filePath + '/result.json'
    f = open(casePath,'r')
    res = f.read()
    data = json.loads(res)
    return data


"""单个case测试,

    Args:
        caseId: 题目ID

    Returns:
        只跑一次，结果存到.mooctest/result.json
        runningTime: 各测试用例运行时间
        runningTimeAvg：测试平均时间
        codeLines：代码行数
        casesResults：测试结果，一个包含0、1的数组，长度为用例数量，用例通过记为1，否则为0
        
"""
def calcuResults(caseId):
    #废案
    #sys.stdin = open('input.txt', 'r')  # 将标准输入重定向为input.txt
    #sys.stdout = open('output.txt', 'w')
    print('-------------测试代码--------------------')
    filePathList=getFilePathList(caseId)

    # 测试用例路径
    casePath = filePathList[1] + '/.mooctest/testCases.json'

    for filePath in filePathList:


        #学生代码路径
        pyPath= filePath +'/main.py'
        f = open(casePath, 'r')
        res = f.read()
        data = json.loads(res)
        caseNum=len(data)
        testRes = {'runningTime': [], 'codeLines': 0, 'casesResults': [],'runningTimeAvg':0}
        #创建用于重定向输入的txt文件
        for idx,case in enumerate(data):
            inputPath=filePath+'/input'+str(idx)+'.txt'
            with open(inputPath,'w')as f:
                f.write(case['input'])

        #以测试用例为输入，运行学生代码，生成测试结果
        runningTime=[]
        for idx in range(caseNum):
            inputPath = filePath + '/input' + str(idx) + '.txt'
            outputPath = filePath + '/output' + str(idx) + '.txt'
            cmd='python'+' '+pyPath+' <'+inputPath+' >'+outputPath # py文件的输入输出重定向到input/output文件中
            start = time.time()
            os.system(cmd)
            end = time.time()
            runningTime.append(end-start)
        testRes['runningTime']=runningTime
        testRes['runningTimeAvg']=np.mean(runningTime)

        #统计测试用例结果
        for idx in range(caseNum):
            outputPath = filePath + '/output' + str(idx) + '.txt'
            output=''
            with open(outputPath, 'r')as f:
                output=f.read()
            if data[idx]['output']==output:
                testRes['casesResults'].append(1)
            else:
                testRes['casesResults'].append(0)

        #统计代码行数
        lineNum=0
        with open(pyPath,'r',encoding='UTF-8') as f:
            lines=f.readlines()
            # for line in lines:
            #     # 除去注释行
            #     realLine = line.lstrip()
            #     if realLine.startswith('#'):
            #         continue
            #     if len(line)>1:
            #         lineNum+=1
            lines=clearCode(lines)
            lineNum=len(lines)
        testRes['codeLines']=lineNum

        resPath = filePath + '/result.json'
        with open(resPath, 'w')as f:
            json.dump(testRes,f)
    print('-------------测试代码完成--------------------')


"""代码评分。

    Args:
        caseId: 题目ID

    Returns:
        评分结果存入data/rated.csv，rate取值区间[0,1]

"""
def rate(caseId):
    print('-------------代码评分--------------------')
    results={'time':[],'lines':[],'path':[]}
    filePathList=getFilePathList(caseId)
    for file in filePathList:
        data = checkResult(file)
        #排除没有全用例通过的代码
        if 0 in data['casesResults']:
            continue
        results['path'].append(file)
        results['time'].append(data['runningTimeAvg'])
        results['lines'].append(data['codeLines'])
    # print(results)
    df=pd.DataFrame(results)
    # print(df)
    # 0-1标准化
    scaler = MinMaxScaler()
    df['time-std'] = scaler.fit_transform(df['time'].values.reshape(-1, 1))
    df['lines-std'] = scaler.fit_transform(df['lines'].values.reshape(-1, 1))
    # print(df)
    # 评分
    df['rate'] = df[['time-std', 'lines-std']].mean(axis=1)
    print(df)
    # 结果存入data/rated.csv
    print('rate')
    Y=[]
    X=[i for i in range(1,len(df['rate'])+1)]
    for i in range(0,len(df['rate'])):
        Y.append(df['rate'][i])
    Y=sorted(Y)
    plt.plot(X,Y,'ob')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(caseId+'题评分排序')
    plt.ylabel('评分')
    plt.show()
    df.to_csv('../cases/'+caseId+'/rated.csv')
    print('-------------代码评分完成--------------------')

"""代码容量度量。

    Args:
        lines: 代码

    Returns:
        代码容量度量值

"""
#todo helstead
def getFunc(lines):
    list1 = []
    for line in lines:
        op = '[=\+\-\*/\[\]\)<>:,%]'
        variable = '\s*[a-zA-Z_]+?[\w_]*\s*'
        if (line.strip().startswith("#")):
            return []
        res = (re.split(op, line))
        re_op1 = r'{}\.{}'.format(variable, variable)
        re_op = r'({})'.format(variable, variable)
        re_def = r'def({})'.format(variable)
        for item in res:
            cur = re.match(re_def, item)
            if (cur != None):
                list1.append(cur.group(1).strip())
                continue
            tmp = re.split('\(', item)
            if (len(tmp) <= 1):
                continue
            for i in range(0, len(tmp) - 1):
                func = tmp[i].strip()
                if (len(func) == 0):
                    continue
                if len(func.split(' '))>1:
                    func=func.split(' ')[-1]
                if (func.startswith('.')):
                    func = func[1:]
                list1.append(func)
    return list(set(list1))
def Helstead(lines):
    # lines=clearCode(lines)
    n1,n2,N1,N2=0,0,0,0
    ops,varibles=[],[] #记录存在的操作符、操作数
    op = '[=\+\-\*/\[\]<>:,%!\(\)]'
    op_list=['+','-','*','/','%','>','<','<=','>=','+=','-=','=','*=','/=','==','!=','!']
    reserved_word=['and','as','break','class','assert','continue','def','del','elif','else'
                  'except','finally','for','from','False','global','if','import','in','is'
                   'lambda','nonlocal','not','None','or','pass','raise','return','try','True'
                   'while','with','yield']
    def_list=getFunc(lines)
    for line in lines:
        for _op in op_list: #检查运算符 如果是+= 会多算+ =一次 后续减掉
            if _op in line :
                ops.append(_op)
                N1+=1
        tmp = re.split(op, line)
        tmp=list(filter(lambda x:x.strip()!='',tmp))
        for item in tmp:
            res=re.split('\s+',item)
            for word in res:
                word=word.strip()
                if word=='' :
                    continue
                if word in reserved_word or word in def_list:
                    N1+=1
                    ops.append(word)
                elif '.' in word:
                    N1+=1
                    if word.startswith('.'):
                        word=word.replace('.','',1)
                    ops.append(word)
                else:
                    N2+=1
                    varibles.append(word)
    special = ['+', '-', '*', '/','=','!']
    special_ = ['+=', '-=', '*=', '/=','==','!=']
    op_count = Counter(ops)
    n1 = len(op_count)
    # print(op_count)
    for i, item in enumerate(special):
        if op_count[special_[i]]!=0 and op_count[item] <= op_count[special_[i]] :
            n1 -= 1
        N1-=op_count[special_[i]]*2
    n2 = len(dict(Counter(varibles)))
    print(list(set(ops)),list(set(varibles)))
    n=n1+n2
    N=N1+N2
    print(N,n)
    return N*log2(n)

if __name__ == '__main__':
    with open('../cases/2307/0/main.py', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        lines=clearCode(lines)
        print(Helstead(lines))

    # rate('2307')




#

#
# # 错误解决ValueError: Expected 2D array, got 1D array instead:
# # array=[4742.92 3398.   2491.9  2149.   2070.  ].
# # Reshape your data either using array.reshape(-1, 1) if your data has a single feature # # or array.reshape(1, -1) if it contains a single sample.
#
# ### 使用array.reshape(-1, 1)重新调整你的数据）python3 加values
#


