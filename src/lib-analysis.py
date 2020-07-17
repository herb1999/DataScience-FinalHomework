# coding=utf-8
"""
统计指定目录下的python文件中包含的import语句
可以指定忽略的目标字符串
放入set中去重，打印
Python 2.7运行通过
"""

import os
from collections import Counter

line_set = []

# 根据你的需要，忽略包含以下字符串的导入语句（一般都是自己开发的测试库）
ignored_strings = ["from lib", "feature", "misc", "testsuite"]


def find_ignore_strings(text, strings):
    result = False
    for target in strings:
        if text.find(target) >= 0:
            result = True
            break
    return result


def visit_dir(arg, dir_name, names):
    for files_path in names:
        file_name = os.path.join(dir_name, files_path)
        if file_name.find('.py') > 0:
            handle_file(file_name)


def handle_file(file_name):
    for text in open(file_name,encoding='utf-8'):
        # 去除两端空格
        text = text.strip()

        # 查找from开头和import开头的行
        if (text.find("from") == 0 and text.find("import") > 0 and
            not find_ignore_strings(text, ignored_strings)) \
                or text.find("import") == 0:
            line_set.append(text)


if __name__ == "__main__":
    # 设置指定目录
    path = "../cases"

    # os.walk(path)
    for root, subdirs, files in os.walk(path):
        for filepath in files:
            file_name=(os.path.join(root, filepath))
            if file_name.find('.py') > 0:
                handle_file(file_name)
        for sub in subdirs:
            file_name=(os.path.join(root, sub))
            if file_name.find('.py') > 0:
                handle_file(file_name)

    result = Counter(line_set)
    print(result)
