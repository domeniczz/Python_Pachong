# -*- codeing = utf-8 -*-
# [url=home.php?mod=space&uid=238618]@Time[/url] : 2021/2/20 16:12
# [url=home.php?mod=space&uid=686208]@AuThor[/url] : 老七疯狂吸氧
# [url=home.php?mod=space&uid=267492]@file[/url] kowyy.py
# @Software:PyCharm
import re
import shutil
import requests
import os
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
}


# 创建文件夹
def creat_dir(dir_name):
    # 判断路径是否存在，若不存在就创建文件夹，若存在就清空文件夹
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)  # 如果该目录不存在就创建它
    else:
        shutil.rmtree(dir_name)  # 存在就删除再创建（清空）
        os.mkdir(dir_name)
    os.chdir(dir_name)  # 切换工作目录到dir_name


# 实现输入单个整数（本程序没有用到这个函数）
def inputInt(content=None):
    while True:
        data = input(content)
        try:
            inputData = eval(data)
            if type(inputData) == int:
                # break
                return inputData
        except:
            pass


# 获取歌曲信息
def get_id(html):
    findlink = re.compile(r'<a href="/song\?id=(\d*)">(.*?)</a></li><li>')
    findname = re.compile(r'<h2 id="artist-name" data-rid=\d* class="sname f-thide sname-max" title=".*?">(.*?)</h2>')
    singername = findname.findall(html)[0]

    creat_dir("网易云下载/" + singername)  # 创建文件夹

    ll = findlink.findall(html)

    print(f"一共有 {len(ll)} 首歌：")

    index = 1
    for n in ll:
        print(index, '\t', n[1])
        index += 1

    # need = inputInt("要下载哪些歌（输入序列号）：")
    # need = ast.literal_eval(input("要下载哪些歌（输入序列号）："))
    
    need = input("要下载哪些歌（输入序列号）：").split()
    need = list(map(int, need))
    
    for i in need:
        download_music(ll[i - 1][1], ll[i - 1][0])
        for j in range(1, 4):
            time.sleep(1)
            print(f"{j}...  ", end='')
        print('')
    # for i in ll:
    #     download_music(i[1], i[0])
    #     time.sleep(0.5)


# 下载音乐
def download_music(name, singer_id):
    url = 'https://music.163.com/song/media/outer/url?id=' + singer_id + '.mp3'
    with open(name + '.m4a', 'wb') as f:
        print('歌曲《', name, '》 下载中 · · · · · · · · · · · · ')
        f.write(requests.get(url=url, headers=headers).content)
        f.close()
        print("《", name, "》下载完成")
        print('')


def main():
    # print('例如：罗大佑的网址是：[url]https://music.163.com/#/artist?id=3686'[/url], '\n', 'ID就是：3686')
    ID = input("请输入歌手ID：")
    url = 'https://music.163.com/artist?id=' + ID
    resp = requests.get(url, headers)
    get_id(resp.text)
    resp.close()


if __name__ == '__main__':
    main()
