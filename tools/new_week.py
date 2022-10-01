#!/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import os.path as fspath
from urllib import request
import json

ques_temp = """---
tags:
---

# 信息
* 题目: [{name}]({link})
* 标签:

# 题解

"""

readme_temp = """# 第{num}场周赛

https://leetcode.cn/contest/weekly-contest-{num}/

## 题目
{ques_list}

"""

ql_temp = """* [{name}]({question_id}.md)"""

def load_week_questions(x):
    with request.urlopen(f"https://leetcode.cn/contest/api/info/weekly-contest-{x}/") as web:
        if web.status != 200:
            return
        data = json.load(web)
        raw_questions = data.get("questions")
        return [
            {
                "question_id": q['question_id'],
                "name": "{question_id}.{title}".format_map(q),
                "link": "https://leetcode.cn/problems/{title_slug}/".format_map(q)
            }
            for q in raw_questions
        ]
def generate(num, path):
    queses = load_week_questions(num)
    if queses is None:
        print("可能没有这一场周赛, 也可能网络错误, 重试下")
        return
    ques_list = list()
    for q in queses:
        ques_list.append(ql_temp.format_map(q))
        fn = fspath.join(path, "{question_id}.md".format_map(q))
        with open(fn, "w") as fd:
            content = ques_temp.format_map(q)
            fd.write(content)
            continue
        print("题目 {question_id} 创建失败".format_map(q))

    with open(fspath.join(path, "Readme.md"), "w") as fd:
        content = readme_temp.format_map({"num":num, "ques_list": "\n".join(ques_list)})
        fd.write(content)
    

def pre(num, path):
    if num < 83:
        raise Exception(f"国内第一场周赛是83")
    if not fspath.exists(path):
        raise Exception(f"目标目录 {path} 不存在")
    dd = fspath.join(path, f"week-{num}")
    try:
        os.makedirs(dd, exist_ok=False)
    except:
        raise Exception(f"周赛目录 {dd} 已经存在")
    return dd

def main():
    parser = argparse.ArgumentParser(description='周赛模板生成器', allow_abbrev=False)
    parser.add_argument('week', type=int, help='哪一周, 国内第一场是83', metavar='week')
    parser.add_argument('--dir', default="<parent>", type=str, help='存哪个目录, 默认上一层', metavar='dir')
    args = vars(parser.parse_args())
    
    week, path = args.get('week', 0), args.get('dir', '<parent>')
    if path == '<parent>':
        path = fspath.dirname(fspath.dirname(__file__))

    try:
        dd = pre(week, path)
    except Exception as e:
        print("\n".join(e.args))
    else:
        generate(week, dd)

if __name__ == '__main__':
    main()
