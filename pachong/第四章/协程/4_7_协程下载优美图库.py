# 用协程下载图片
# 结合 bs4

# 1.拿到主页面的源代码. 然后提取到子页面的链接地址, href
# 2.通过href拿到子页面的内容. 从子页面中找到图片的下载地址 img -> src
# 3.下载图片

from bs4 import BeautifulSoup
import time
import asyncio
import aiohttp
import aiofiles

url = "https://www.umei.cc/bizhitupian/weimeibizhi/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}


# 用 bs4 获取图片链接
async def get_url():
    src_list = []
    async with aiohttp.ClientSession() as session:  # aiohttp.ClientSession() 等价于 requests 模块
        async with session.get(url, headers=headers) as resp:
            main_page = BeautifulSoup(await resp.text(), "html.parser")  # bs4 解析网页
            a_list = main_page.find("div", attrs={"class": "TypeList"}).find_all("a")
            for a in a_list:
                href = a.get('href')  # 获取到子页面的地址

                # 拿到子页面的源代码
                async with session.get(url + href.split("/")[3], headers=headers) as child_page_resp:
                    child_page_resp.encoding = 'utf-8'
                    child_page_text = await child_page_resp.text()
                    # 解析子页面
                    child_page = BeautifulSoup(child_page_text, "html.parser")
                    p = child_page.find("p", align="center")
                    img_src = p.find("img").get("src")
                    src_list.append(img_src)

    return src_list


async def download(img_src):
    name = img_src.split("/")[-1]
    # file_format = url.rsplit(".", 1)[1]
    file_format = img_src.split(".")[-1]
    async with aiohttp.ClientSession() as session:  # aiohttp.ClientSession() 等价于 requests 模块
        async with session.get(img_src, headers=headers) as resp:  # resp == requests.get()
            # resp.content.read() 等价于 requests 里面的 resp.content
            # resp.text() 等价于 requests 里面的 resp.text
            # resp.json() 等价于 requests 里面的 resp.json()
            async with aiofiles.open(f"../img/{name[0:5] + '.' + file_format}", mode="wb") as img:
                await img.write(
                    await resp.content.read())  # resp.content.read()读取内容需要挂起，为异步，因为是什么时候有内容什么时候读取

                print(name[0:5] + '.' + file_format + ' Download complete')


async def main():
    src_res_list = await asyncio.wait([asyncio.create_task(get_url())])
    src_res_list = src_res_list[0].pop().result()  # 获取函数的返回值
    print(src_res_list)
    tasks = []
    for src in src_res_list:
        # print(src)
        tasks.append(asyncio.create_task(download(src)))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    start = time.time()

    # 下面这行代码是为了防止报错： RuntimeError: Event loop is closed
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())

    end = time.time()
    print("Time elapsed: ", end - start)


# -------------------- $ 以下代码是 下载指定三张图片 $ -------------------- #

# urls = [
#     "http://kr.shanghai-jiuxin.com/file/2020/1031/191468637cab2f0206f7d1d9b175ac81.jpg",
#     "http://kr.shanghai-jiuxin.com/file/2020/1031/a2c58d6d726fb7ef29390becac5d8643.jpg",
#     "http://kr.shanghai-jiuxin.com/file/2020/1031/563337d07af599a9ea64e620729f367e.jpg"
# ]
#
#
# async def download(s):
#     # 发送请求
#     # 得到图片内容
#     # 保存到文件
#     # name = url.rsplit("/", 1)[1]  # url对象的方法rsplit是从右边开始切切, 1表示切一次. 得到[1]位置的内容
#     name = s.split("/")[-1]
#     # file_format = url.rsplit(".", 1)[1]
#     file_format = s.split(".")[-1]
#     async with aiohttp.ClientSession() as session:  # aiohttp.ClientSession() 等价于 requests 模块
#         async with session.get(s, headers=headers) as resp:  # resp == requests.get()
#             # resp.content.read() 等价于 requests 里面的 resp.content
#             # resp.text() 等价于 requests 里面的 resp.text
#             # resp.json() 等价于 requests 里面的 resp.json()
#             async with aiofiles.open(f"img/{name[0:5] + '.' + file_format}", mode="wb") as img:
#                 await img.write(await resp.content.read())  # resp.content.read()读取内容需要挂起，为异步，因为是什么时候有内容什么时候读取
#
#                 print(name[0:5] + '.' + file_format + ' Download complete')
#
#
# async def main():
#     tasks = [asyncio.create_task(download(url)) for url in urls]
#     await asyncio.wait(tasks)
#
#     # 第二种写法
#     # tasks = []
#     # for url in urls:
#     #     tasks.append(download(url))
#     #
#     # await asyncio.wait(tasks)
#
#
# if __name__ == '__main__':
#     # 防止报错 RuntimeError: Event loop is closed
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#
#     asyncio.run(main())
