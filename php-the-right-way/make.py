#!/usr/bin/env python
# coding:utf-8

# 读取文件列表

# 分析文件名 `a-b-c-name.md`
# - 如果`b==01`,说明这是个开头
# - 如果a与上一个a一样，说明要合并到前一个

# 读取文件内容
# - 去除头部信息
# - 获取文件标题，第一个h1标签`# title` or `## title`


from path import Path
import os
import re
import codecs
import shutil

source_path = u'./php-the-right-way/_posts/'  # markdown文件源
dest_path = u'./dist'  # 生成到

if os.path.exists(dest_path):
    shutil.rmtree(dest_path)

os.mkdir(dest_path)

p = Path(source_path)

regex_title = re.compile(r'^[#]+(.*){#')


def __get_real_content_lines(file_path):
    """
    获得文件(jekyll)主体内容
    :param file_path:
    :return:
    """
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
            return lines[i:]

    return lines


def parser_file_name(file_path):
    """
    解析文件名
    :param file_path:
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
        'content': u''.join(content_lines)
    }


def get_file_title(file_path):
    """
    从文件内容提取文件标题
    :param file_path:
    :return:
    """
    lines = __get_real_content_lines(file_path)
    return regex_title.findall(lines[0])[0].strip(' ')


def filter_content(content):
    """
    过滤/修正部分字符串
    :param content:
    :return:
    """
    regex_highlight = re.compile(r'(\{% highlight ([a-zA-Z]+) %\}){1}')

    for x in regex_highlight.findall(content):
        content = content.replace(x[0], '```%s' % x[1])

    return content.replace('{% endhighlight %}', '```')


def write_file(dir_name, name, content):
    """
    写入文件
    :param dir_name: 目录名
    :param name: 文件名
    :param content: 内容
    """
    with codecs.open(os.path.join(dest_path, dir_name, name + u'.md'), mode='w', encoding='utf-8') as f:
        f.write(content)


def main():
    cur_dir = ''
    cur_a = '0'
    cur_b = '0'
    cur_c = '0'

    dir_index = 1
    file_index = 0

    for f in p.listdir():
        file_info = parser_file_name(f)
        file_info['content'] = filter_content(file_info['content'])

        title = get_file_title(f)

        file_index += 1
        if file_info['b'] == '01':
            cur_dir = '%04d-%s' % (dir_index, title)
            os.mkdir(os.path.join(dest_path, cur_dir))
            dir_index += 1
            file_index = 1

        write_file(cur_dir, u'%04d-%s' % (file_index, title), file_info['content'])

    print('Finish!')


if __name__ == '__main__':
    main()

