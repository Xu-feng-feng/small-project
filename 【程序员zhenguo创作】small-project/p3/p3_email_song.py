# encoding: utf-8
"""
@file: p3_email_song.py
@desc: 定时、自动爬取网易今日推荐歌单，并自动发送邮件
@author: zhen guo
@time: 2021/12/30
"""
import time
import re
import smtplib
from email import header
from email.mime import text, multipart
from threading import Timer
from DecryptLogin import login
from DecryptLogin.core.music163 import Cracker
import click

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Accept': '*/*'
}
send_email_interval = 60*60*24

class NetRcmndSong():
    def __init__(self, username, password):
        username = username
        password = password
        self.username = username
        self.session = NetRcmndSong.__login(username, password)
        self.csrf = re.findall('__csrf=(.*?) for', str(self.session.cookies))[0]
        self.cracker = Cracker()
        self.headers = headers
        self.title = None
        self.email_content = None

    def run(self):
        recommend_info = self.__get_recommend()
        keys, values = list(recommend_info.keys()), list(recommend_info.values())
        self.title = f'【程序员zhenguo】和网易云音乐今日为你({self.username})推荐的歌曲如下:'
        options = [v for v in values]
        self.email_content = self.title + "\n" + '\n'.join(options) + "\n\n\t来自你的老朋友\n\t程序员zhenguo"
        print(self.email_content)
        self.__send_email()

    @staticmethod
    def __login(username, password):
        """
        模拟登录
        :param username:
        :param password:
        :return:
        """
        lg = login.Login()
        _, session = lg.music163(username, password)
        return session

    def __get_recommend(self):
        """
        获得每日歌曲推荐
        :return:
        """
        url = 'http://music.163.com/weapi/v2/discovery/recommend/songs?csrf_token='
        data = {
            'crsf_token': self.csrf,
            'limit': '999',
            'offset': '0',
            'total': 'true'
        }
        data = self.cracker.get(data)
        response = self.session.post(url, headers=self.headers, data=data)
        response_json = response.json()
        daily_recommend_info = {}
        if response_json['code'] == 200:
            for i, item in enumerate(response_json['recommend']):
                song_name = item['name']
                song_id = item['id']
                singer = item['artists'][0]['name']
                daily_recommend_info[song_id] = f'{i} {song_name}-{singer}'
            return daily_recommend_info
        else:
            raise RuntimeError('获取每日歌曲推荐失败, 请检查网络并重新运行程序...')

    def __send_email(self):
        smt_p = smtplib.SMTP()
        smt_p.connect(host='smtp.qq.com', port=25)
        # 这是我的QQ邮箱用户名和授权码
        sender, auth_code = '113097485@qq.com', "zkgqtddtmlehbiaj"
        smt_p.login(sender, auth_code)
        # 添加收件人到配置文件中
        with open('song_email.txt', 'r') as fr:
            receiver_addresses = fr.readlines()
        if len(receiver_addresses) == 0:
            return
        receiver_addresses = list(map(lambda x: re.sub(r'\s', '', x), receiver_addresses))
        for email_address in receiver_addresses:
            try:
                msg = multipart.MIMEMultipart()
                msg['From'] = "程序员zhenguo(爬取网易云音乐)"
                msg['To'] = email_address
                msg['subject'] = header.Header(self.title, 'utf-8')
                msg.attach(text.MIMEText(self.email_content, 'plain', 'utf-8'))
                smt_p.sendmail(sender, email_address, msg.as_string())
                time.sleep(10)
            except Exception as e:
                print(e)
        smt_p.quit()

@click.command()
@click.option('-u', help='用户名')
@click.option('-p', help='密码')
def cmd(u, p):
    client = NetRcmndSong(u, p)
    client.run()
    Timer(send_email_interval, cmd()).start()


if __name__ == '__main__':
    cmd()
