# encoding: utf-8
"""
作者：程序员zhenguo
公众号、视频号、抖音同名：程序员zhenguo
个人网站：www.zglg.work

功能：自动生成指定长度的密码
使用说明：
1. 命令行启动：python pwd_gen.py
默认密码长度为10，密码彻底乱序
2. 参数：
python pwd_gen.py -len=15 -shuf=False
生成15位密码，按照英文字符+数字+特殊字符格式
"""

import random
import string
import click

alpha_all = string.ascii_letters
alpha = alpha_all[:26]
num = string.digits
special = "@#$%&*"


class PwdGenerator:
    def __init__(self, pass_len, is_shuffle=True):
        if pass_len <= 0:
            raise ValueError("密码长度不能小于0")
        self.pass_len = pass_len
        self.alpha_len = max(pass_len // 2, 1)
        self.num_len = pass_len * 30 // 100
        self.special_len = pass_len - (self.alpha_len + self.num_len)
        self.__password = []
        self.is_shuffle = is_shuffle

    def gen_pwd(self):
        """
        生成密码
        """
        # 生成英文字符部分
        self.__generate_pass(self.alpha_len, alpha, True)
        # 生成数字部分
        self.__generate_pass(self.num_len, num)
        # 生成特殊字符部分
        self.__generate_pass(self.special_len, special)
        # 打乱顺序
        if self.is_shuffle:
            random.shuffle(self.__password)
        return ''.join(self.__password)

    def __generate_pass(self, length, array, is_alpha=False):
        for i in range(length):
            index = random.randint(0, len(array) - 1)
            character = array[index]
            if is_alpha:
                # 50%概率转化大写
                case = random.randint(0, 1)
                if case == 1:
                    character = character.upper()
            self.__password.append(character)


@click.command()
@click.option('-len', default=10, help='密码长度')
@click.option('-shuf', default=True, help='打乱')
def cmd(len, shuf):
    print(PwdGenerator(len, shuf).gen_pwd())


if __name__ == "__main__":
    cmd()
