#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from memory_profiler import profile
from guppy import hpy
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
def checkTestCode(caseId,code):
    bingo=0
    path = '../cases/' + caseId + '/testCode'
    casePath='../cases/'+caseId+'/1/.mooctest/testCases.json'
    pyPath = path+'/testCode.py'
    f = open(casePath, 'r')
    res = f.read()
    data = json.loads(res)
    caseNum = len(data)
    for idx, case in enumerate(data):
        inputPath = path + '/input' + str(idx) + '.txt'
        with open(inputPath, 'w')as f:
            f.write(case['input'])
    for idx in range(caseNum):
        inputPath =  path+ '/input' + str(idx) + '.txt'
        outputPath = path + '/output' + str(idx) + '.txt'
        cmd = 'python' + ' ' + pyPath + ' <' + inputPath + ' >' + outputPath  # py文件的输入输出重定向到input/output文件中
        os.system(cmd)
    for idx in range(caseNum):
        outputPath = path + '/output' + str(idx) + '.txt'
        output = ''
        with open(outputPath, 'r')as f:
            output = f.read()
        if data[idx]['output'] == output:
            bingo+=1
    print(bingo*100/caseNum)
    return bingo*100/caseNum

def calcuResults(caseId):
    #废案
    #sys.stdin = open('input.txt', 'r')  # 将标准输入重定向为input.txt
    #sys.stdout = open('output.txt', 'w')
    print('-------------测试代码--------------------')
    filePathList=getFilePathList(caseId)


    # 测试用例路径
    casePath = filePathList[1] + '/.mooctest/testCases.json'

    for filePath in filePathList:
        print('testing '+filePath)

        #学生代码路径
        pyPath= filePath +'/main.py'
        f = open(casePath, 'r')
        res = f.read()
        data = json.loads(res)
        caseNum=len(data)
        testRes = {'runningTime': [], 'volnum': 0, 'casesResults': [],'runningTimeAvg':0}

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

        # 测试代码内存占用
        # for idx in range(caseNum):
        #     memory_tracker(filePath,idx)

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

        # 面向用例编程的检测
        #   1.获取测试用例的全部输出
        outputs=[case['output'] for case in data]
        #   2.检测代码中有没有全部的测试用例
        with open(pyPath,'r',encoding='UTF-8') as f:
            lines=f.readlines()
            lines=clearCode(lines)
            for line in lines:
                for output in outputs:
                    if output in ['F','T','True','False','true','false']:
                        continue
                    testStr1='print(\''+output[:-1]+'\')'
                    testStr2 = 'print(\"' + output[:-1] + '\")'
                    if testStr1 in line or testStr2 in line:
                        testRes['casesResults'] = [0] * caseNum
                        print('----------------------------------------cheater: ' + filePath)
                        break

        #统计代码容量、循环深度
        with open(pyPath,'r',encoding='UTF-8') as f:
            lines=f.readlines()
            lines=clearCode(lines)
            volnum=Helstead(lines)
            # depth=getDepth(lines)
        testRes['volnum']=volnum
        # testRes['depth'] = depth


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
    results={'time':[],'volnums':[],'path':[]}
    filePathList=getFilePathList(caseId)
    for file in filePathList:
        data = checkResult(file)
        #排除没有全用例通过的代码
        if 0 in data['casesResults']:
            continue
        results['path'].append(file)
        results['time'].append(data['runningTimeAvg'])
        results['volnums'].append(data['volnum'])
        # results['loopDepth'].append(data['depth'])
    # print(results)
    df=pd.DataFrame(results)
    # print(df)
    # 0-1标准化
    scaler = MinMaxScaler()
    df['time-std'] = scaler.fit_transform(df['time'].values.reshape(-1, 1))
    df['volnums-std'] = scaler.fit_transform(df['volnums'].values.reshape(-1, 1))
    # df['loopDepth-std'] = scaler.fit_transform(df['loopDepth'].values.reshape(-1, 1))
    # print(df)
    # 评分
    df['rate'] = df[['time-std', 'volnums-std']].mean(axis=1)
    df=df.sort_values(by='rate')
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
    plt.xlabel('代码标号')
    plt.show()
    df.to_csv('../cases/'+caseId+'/rated.csv')
    print('-------------代码评分完成--------------------')

"""代码容量度量。

    Args:
        lines: 代码

    Returns:
        代码容量度量值

"""
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
    # print(list(set(ops)),list(set(varibles)))
    n=n1+n2
    N=N1+N2
    # print(N,n)
    return N*log2(n)


# @profile(precision=4, stream=open('../temp/memory_profiler.log','w+',encoding='gbk'))
# def memory_tracker(filePath,idx):
#     pyPath = filePath + '/main.py'
#     inputPath = filePath + '/input' + str(idx) + '.txt'
#     outputPath = filePath + '/memory' + str(idx) + '.txt'
#     cmd = 'python ' + '-m memory_profiler ' + pyPath + ' <' + inputPath
#     os.system(cmd)
#     pass
"""用于追踪代码内存占用

args:
    filePath:代码目录
    idx:第几个用例
"""
def memory_tracker(filePath,idx):
    pyPath = filePath + '/main.py'
    inputPath = filePath + '/input' + str(idx) + '.txt'
    outputPath = filePath + '/memory' + str(idx) + '.txt'
    cmd = 'mprof run ' + pyPath + ' --python '+'< ' + inputPath
    os.system(cmd)
    for root, dirs, files in os.walk('./'):
        for file in files:
            if os.path.splitext(file)[1] == '.dat':
                with open(file,'r') as f:
                    m=f.readlines()[-1]
                    with open('../data/test.txt','a+') as f:
                        f.write(m)
    os.system('mprof clean')

def getDepth(lines):
    depths=[]
    tmplines=[]
    mainlines=[]
    isDef=False
    defBegin=0
    for line in lines:
        if line.startswith("def"):
            isDef=True
            defBegin=line.index('d')
            continue
        if isDef:
            if line.index(line.strip()[0])==defBegin:
                isDef=False
                depth=roundDepth(tmplines)
                depths.append(depth)
                tmplines=[]
            else:
                tmplines.append(line)
        else:
            mainlines.append(line)
    if mainlines!=[]:
        depths.append(roundDepth(mainlines))
    depths.sort()
    return depths[-1]
def roundDepth(lines):
    dic={}
    for line in lines:
        times = line.count('for') + line.count('while')  # 该行for\while出现次数
        if times==0:
            continue
        idx=line.index(line.strip()[0])
        if (idx not in dic.keys() or dic[idx]<times):
            dic[idx]=times
    l=dic.keys()
    depths=[]
    for i,item in enumerate(l):
        depths.append(i+dic[item])
    if depths==[]:
        return 0
    depths.sort()
    return depths[-1]

if __name__ == '__main__':
    # with open('../cases/2307/4/main.py', 'r', encoding='UTF-8') as f:
    #     lines = f.readlines()
    #     lines=clearCode(lines)
    #     print(getDepth(lines))

    # calcuResults('2307')
    rate('2908')
    # hpy().heap()
    # memory_tracker('../cases/2176/2/main.py',0)




#

#
# # 错误解决ValueError: Expected 2D array, got 1D array instead:
# # array=[4742.92 3398.   2491.9  2149.   2070.  ].
# # Reshape your data either using array.reshape(-1, 1) if your data has a single feature # # or array.reshape(1, -1) if it contains a single sample.
#
# ### 使用array.reshape(-1, 1)重新调整你的数据）python3 加values
#


