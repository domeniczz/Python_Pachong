# 1.拿到主页面的源代码. 然后提取到子页面的链接地址, href
# 2.通过href拿到子页面的内容. 从子页面中找到图片的下载地址 img -> src
# 3.下载图片

import requests
from bs4 import BeautifulSoup
import time

t_start = time.time()

url = "https://www.umei.cc/bizhitupian/weimeibizhi/"

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

resp = requests.get(url, headers=headers)
resp.encoding = 'utf-8'  # 处理乱码

# print(resp.text)

# 把源代码交给bs
main_page = BeautifulSoup(resp.text, "html.parser")
alist = main_page.find("div", class_="TypeList").find_all("a")
# print(alist)

for a in alist:
    href = a.get('href')  # 直接通过get，获取到子页面的地址

    # 拿到子页面的源代码
    child_page_resp = requests.get(url + href.split("/")[3])
    child_page_resp.encoding = 'utf-8'
    child_page_text = child_page_resp.text

    # 从子页面中拿到图片的下载路径
    child_page = BeautifulSoup(child_page_text, "html.parser")
    p = child_page.find("p", align="center")
    img = p.find("img")
    src = img.get("src")

    # 下载图片
    img_resp = requests.get(src)
    # img_resp.content  # 这里拿到的是字节
    img_name = src.split("/")[-1]  # 拿到url中的最后一个/以后的内容

    with open("img/" + img_name, mode="wb") as f:
        f.write(img_resp.content)  # 图片内容写入文件

    print("over!!!", img_name)
    time.sleep(1)

print("all over!!!")


t_over = time.time()
print(t_over - t_start)  # 打印程序执行的总时长
