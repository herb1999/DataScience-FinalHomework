import re
import pandas as pd
variable='\s*[a-zA-Z_]+?[\w_]*\s*'
lambda_name='lambda (.*){1}'
function_name=variable+'|'+lambda_name
Negative='\s*-?\d+\s*'
a_list='\[{}(,{})*\]'.format(Negative,Negative)

#todo:zjy

# 1.选最大值
re_max1=re.compile(r'^'+variable+'\=\s*max\(.*\)$')
re_max2=re.compile(r'^'+variable+'\=.+if.+else.+')
re_max3=re.compile(r'^'+variable+'\=\s*\[.*\]\[.*\]')

# 2.值交换 元组赋值
re_value_change=re.compile(r'^{}(,{})*\=.+'.format(variable,variable))

# 3.循环与else匹配用于在循环正常结束和循环条件不成立时执行
# todo

# 4.切片操作
re_split1=re.compile(r'^{}={}\[{}(:{})+\]'.format(variable,variable,Negative,Negative))

# 5.推导表达式 for..in
re_derivation=re.compile(r'^{}\=\s*\[.+for{}in{}\]'.format(variable,variable,variable))

#6.list先按一个属性排列，再按另外一个属性排列
re_sort=re.compile(r'{}|{}\.sort\(key=lambda.+\)'.format(variable,a_list))

#7.filter：函数接受两个参数，第一个是过滤函数，第二个是可遍历的对象，用于选择出所有满足过滤条件的元素

re_filter=re.compile(r'{}=filter\(.+\)'.format(variable))
#匹配不全 待解决
print(re.match(re_filter,'s=filter(lambda x:not str(x).islower(),"adsssssddddd")'))

#8.map：用于把函数作用于可遍历对象的每一个元素。类似于数学中映射的概念
re_map=re.compile(r'{}=map\(.+\)'.format(variable))

#9.生成器
re_generator=re.compile(r'{}=\s*\(.*for{}in.*'.format(variable,variable))

#10.with
re_with=re.compile(r'with.+as{}:'.format(variable))

#11.from..import..
re_import=re.compile(r'from{}import({})'.format(variable,variable))
#re.match(re_import,'from functools import reduce').group(1)即可获得导入的方法

print(re.match(re_generator,'list = ( a for a in b )').group(0))

regFunctions={
    'generator':re_generator,
    'max1':re_max1,
    'max2':re_max2,
    'max3':re_max3,
    'value_change':re_value_change,
    'split':re_split1,
    'derivation':re_derivation,
    'sort':re_sort,
    'filter':re_filter,
    'map':re_map,
    'with':re_with,
}

