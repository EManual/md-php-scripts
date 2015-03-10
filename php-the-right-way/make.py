#!/usr/bin/env python
# coding:utf-8

# 读取文件列表

# 分析文件名 `a-b-c-name.md`
# - 如果`b==01`,说明这是个开头
# - 如果a与上一个a一样，说明要合并到前一个

# 读取文件内容
# - 去除头部信息
#   - 获取文件标题，第一个h1标签`# title` or `## title`


from path import Path
import os
import sys
import re
import codecs

source_path = u'./php-the-right-way/_posts/'  # markdown文件源
dest_path = u'./dist'  # 生成到

p = Path(source_path)

regex_title = re.compile(r'^[#]+(.*){#')


def __get_real_content_lines(file_path):
    with codecs.open(file_path, encoding='utf-8') as f:
        lines = f.readlines()
        if '---' in lines[0]:
            i = 1
            while not '---' in lines[i]:
                i += 1
            i += 1

            # 移除第一个标题前的所有空行
            regex_white_space = re.compile('^\s+$')
            while '' == regex_white_space.sub('', lines[i]):
                i += 1
            # print ''.join(lines[i:])
            return lines[i:]

    return lines


def parser_file_name(file_path):
    """
    解析文件名
    :param file_path:
    :return:
    """
    # print os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    spliters = filename.split('-')

    content_lines = __get_real_content_lines(file_path)

    # 移除第一标题的anchor
    regex_rm_anchor = re.compile('^(.*){#.*}')
    # print regex_rm_anchor.findall(content_lines[0])[0]
    content_lines[0] = regex_rm_anchor.findall(content_lines[0])[0]


    return {
        'a': spliters[0],
        'b': spliters[1],
        'c': spliters[2],
        'content': ''.join(content_lines)
    }


def get_file_title(file_path):
    lines = __get_real_content_lines(file_path)
    # print regex_title.findall(lines[0])
    return regex_title.findall(lines[0])[0].strip(' ')


for f in p.listdir():
    file_info = parser_file_name(f)
    title = get_file_title(f)

    print title
    print file_info['content']
    # break
