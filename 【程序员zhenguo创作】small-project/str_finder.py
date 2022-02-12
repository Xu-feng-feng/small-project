# encoding: utf-8
"""
作者：程序员zhenguo
公众号、视频号、抖音同名：程序员zhenguo
个人网站：www.zglg.work

功能：递归查找指定路径下包括指定文本的文件
使用说明：
1. 必须命令行启动：python str_finder.py
"""

import os
import threading
import click


@click.command()
@click.option('-t', help='要查找的文本')
@click.option('-p', help='在哪里查找')
def __cmd(t, p):
    TextFinder(t, p).get_files()


class TextFinder:
    max_thread_cnt = 500  # 同时存活线程数最大500
    big_byte_file = 0.05  # MB
    ext_list = ['.csv', '.txt', '.md', '.py', '.java']

    def __init__(self, text, path):
        self.text = text
        self.path = path
        self.result = []
        self.threads = []
        self._live_thread_cnt = 0

    def get_files(self):
        self.__get_files(self.path)
        for thr in self.threads:
            thr.join()

        print('-' * 100)
        print(f'共使用{len(self.threads)}个线程')
        print(f'同时存活线程数{self._live_thread_cnt}')
        if len(self.result) == 0:
            print(self.text + " not found! ")
        else:
            for res in self.result:
                print(res)

    def __get_files(self, path):
        files = os.listdir(path)
        for name in files:
            path_name = os.path.join(path, name)
            if os.path.isdir(path_name):
                self.__get_files(path_name)
            if self.__in_extensions(name):
                file_byte = os.stat(path_name).st_size / 1024 / 1024
                if file_byte > TextFinder.big_byte_file:
                    if threading.active_count() < TextFinder.max_thread_cnt:
                        big_file_proc = threading.Thread(target=self.__task, args=(path_name,))
                        big_file_proc.start()
                        self.threads.append(big_file_proc)
                        self._live_thread_cnt = max(self._live_thread_cnt, threading.active_count())
                    else:
                        self.__task(path_name)
                else:
                    self.__task(path_name)

    def __task(self, path_name):
        print(f'正在查找 {path_name}')
        f = open(path_name, "r")
        try:
            if self.text in f.read():
                self.__found_flag = True
                self.result.append(f'{self.text} found in {path_name}')
        except UnicodeDecodeError:
            print(f'解析错误 {path_name}')

    def __in_extensions(self, file_name):
        return any(file_name.endswith(ext) for ext in TextFinder.ext_list)


if __name__ == "__main__":
    __cmd()
