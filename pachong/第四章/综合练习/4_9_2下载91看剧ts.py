# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 10:03:30 2021

@author: Domenic

流程:
    1. 拿到548121-1-1.html的页面源代码
    2. 从源代码中提取到m3u8的url
    3. 下载m3u8
    4. 读取m3u8文件, 下载视频
    5. 合并视频
"""

"""
网页上面的视频，一定是用 video 标签显示的
如果页面源代码中没有 video 标签，那就可能是由 script 来生成 video 标签

这里的案例
我们 ctrl+U 访问页面源代码后，可以在 script 里面找到 video 和 m3u8 链接

如果源代码里面没有 m3u8 链接
那么可能是用到了 iframe (视频播放应用了其他的网页，相当于网页嵌套了另外一个网页）
可以 F12 进入检查，找到视频网页的 iframe 的源地址(src)
"""

import os
import shutil
import requests
import re


# 创建文件夹
def creat_dir(dir_name):
    # 判断路径是否存在，若不存在就创建文件夹，若存在就清空文件夹
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)  # 如果该目录不存在就创建它
    else:
        shutil.rmtree(dir_name)  # 存在就删除再创建（清空）
        os.mkdir(dir_name)
    os.chdir(dir_name)  # 切换工作目录到dir_name


url = "https://www.91kanju2.com/vod-play/61304-1-1.html"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
}


"""
获取m3u8的访问链接
"""
resp = requests.get(url, headers)
print("网页请求成功！")
# print(resp.text)

video = re.compile(r"url: '(?P<link>.*?)',", re.S)  # 用来提取m3u8的url地址
title = re.compile(r"<title>(?P<title>.*?)</title>", re.S)

m3u8_link = video.search(resp.text).group("link").strip()
title = title.search(resp.text).group("title").split("－")[0]
# print(m3u8_link)


"""
下载m3u8文件
"""
resp2 = requests.get(m3u8_link, headers=headers)
with open(f"{title}.m3u8", mode="wb") as f:  # binary模式，不能添加encoding参数
    f.write(resp2.content)

resp2.close()
print("m3u8下载完成！")


"""
解析m3u8，下载视频
"""
i = 0
f = open(f"{title}.m3u8", mode="r", encoding="UTF-8")
creat_dir("videoClips")
# for循环来对文件内容逐行循环
for line in f:
    line = line.strip()
    if line.startswith('#'):
        continue
    else:
        if i == 3:
            break
        print(f"第{i}个片段......", end='')
        resp3 = requests.get(line, headers=headers)
        with open(f"{i}.ts", mode="wb") as video_clips:
            video_clips.write(resp3.content)
        resp3.close()
        i += 1
        print("下载完成")
f.close()

"""
合并视频：

可以在ts文件夹下面打开cmd命令行
使用命令：copy /b *.ts new.ts
       copy /b 1.ts+2.ts+3.ts new.ts
或者：   copy /b *.ts new.mp4 直接产生.mp4文件
这样就好生成一个new.ts文件，是合并版本，potplayer可以直接播放
"""
