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
* 题目: [{question_name}]({question_link})
* 标签:

# 题解

"""

readme_temp = """# 第{week}场周赛

{page}

## 题目
{question_list}
"""

ql_temp = """* [{question_name}]({question_id}.md)"""

class Week:
    def __init__(self, bi=False, num=0):
        self.__bi = bi
        self.__num = num
    @property
    def is_biweek(self):
        return self.__bi
    @property
    def week(self):
        return self.__num
    @property
    def api(self):
        if self.is_biweek:
            return "https://leetcode.cn/contest/api/info/biweekly-contest-{}/".format(self.week)
        else:
            return "https://leetcode.cn/contest/api/info/weekly-contest-{}/".format(self.week)
    @property
    def page(self):
        if self.is_biweek:
            return "https://leetcode.cn/contest/biweekly-contest-{}/".format(self.week)
        else:
            return "https://leetcode.cn/contest/weekly-contest-{}/".format(self.week)
    @property
    def name(self):
        if self.is_biweek:
            return "biweek-{}".format(self.week)
        else:
            return "week-{}".format(self.week)

def load_week_questions(week:Week):
    with request.urlopen(week.api) as web:
        if web.status != 200:
            raise Exception("网络错误, 可以手动打开周赛页面{}检查是否有效".format(week.page))
        data = json.load(web)
        raw_questions = data.get("questions", None)
        if not raw_questions:
            raise Exception(data.get("error", "竞赛不存在"))
        return [
            {
                "question_id": q['question_id'],
                "question_name": "{question_id}.{title}".format_map(q),
                "question_link": "https://leetcode.cn/problems/{title_slug}/".format_map(q)
            }
            for q in raw_questions
        ]

def generate(week:Week, path:str):
    try:
        queses = load_week_questions(week)
    except Exception as e:
        print("\n".join(e.args))
        return

    try:
        os.makedirs(path)
    except:
        print(f"周赛目录 {path} 创建失败")
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
        content = readme_temp.format_map({"week":week.week, "question_list": "\n".join(ques_list), "page":week.page})
        fd.write(content)
    
def pre(week:Week, path):
    if not fspath.exists(path):
        raise Exception(f"目标目录 {path} 不存在")
    dd = fspath.join(path, week.name)
    if fspath.exists(dd):
        raise Exception(f"周赛目录 {dd} 已经存在")
    return dd

def week_parse(raw:str):
    bi = False
    s = raw
    if s.startswith("b"):
        s = s[1:]
        bi = True
    try:
        week = int(s, 10)
        if not bi and week < 83:
            raise Exception("国内第一场单周赛是83")
        elif bi and week < 1:
            raise Exception("双周赛场次编号从1开始")
        return Week(bi, week)
    except ValueError:
        msg = "场次编号 {} 格式有误, 单周: `编号`, 双周: `b编号`".format(raw)
        raise argparse.ArgumentTypeError(msg)
    except Exception as e:
        raise argparse.ArgumentTypeError(*e.args) 

def main():
    parser = argparse.ArgumentParser(description='周赛模板生成器', allow_abbrev=False)
    parser.add_argument('week', type=week_parse, help='哪一周, 国内第一场是83, 双周赛使用 `b编号` ', metavar='week')
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
