"""
作者：程序员zhenguo
公众号、视频号、抖音同名：程序员zhenguo
个人网站：www.zglg.work
功能：自动生成100个测试文件
使用说明：首先pip 安装faker（pip install faker)
再安装pandas，执行 pip install pandas

最后修改excel文件保存路径（D:\办公自动化\考试分数）为你的文件目录
"""
import os
import random
from faker import Faker
import pandas as pd

fake = Faker("zh_CN")


def auto_gen_excel(file_path, file_n=100):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    for i in range(file_n):
        nn = random.randint(3, 10)
        names = [fake.name()
                 for _ in range(nn)]
        grades = [random.randint(50, 100)
                  for _ in range(nn)]
        d = {'姓名': names, '考试分数': grades}
        file = os.path.join(file_path, f'班级{i + 1}.xlsx')
        pd.DataFrame(d).to_excel(file, index=False)
    print("Done")

if __name__ == "__main__":
    auto_gen_excel('D:\办公自动化\考试分数2')
