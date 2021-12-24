# 网站是PC版的百度小说 搜索页网址：https://dushu.baidu.com/pc/search
# 西游记的网址：https://dushu.baidu.com/pc/reader?gid=4306063500

import json
import asyncio
import aiohttp
import aiofiles
import os
import shutil

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}


# 创建文件夹
def creat_dir(dir_name):
    # 判断路径是否存在，若不存在就创建文件夹，若存在就清空文件夹
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)  # 如果该目录不存在就创建它
    else:
        shutil.rmtree(dir_name)  # 存在就删除再创建（清空）
        os.mkdir(dir_name)
    os.chdir(dir_name)  # 切换工作目录到dir_name


# 模拟搜索，获取到书本的book_id
async def search():
    while True:
        book = input("Input Book Name: ")
        data = {
            "word": book,
            "pageNum": 1
        }

        # 判断路径是否存在，若不存在就创建文件夹，若存在就清空文件夹
        path = f"../novel/{book}"
        creat_dir(path)

        search_url = f"https://dushu.baidu.com/api/pc/getSearch?data={json.dumps(data)}"
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers) as res:
                search_res_list = (await res.json())["data"]["list"]
                index = 0
                for s in search_res_list:
                    print(index, "Author：" + s["author"], "Book Name：" + s["book_name"], )
                    index += 1

                if index == 0:  # 如果没有任何书
                    print("Find none! Search again.")
                    continue
                else:
                    if input("Have you find the book? (Y/N) ") == 'N':  # 如果没有想要的书
                        print("Fine, search again.")
                        continue
                    else:
                        # 用户输入序号，返回book_id
                        return search_res_list[int(input("Input The Book Index You Want: "))]["book_id"]


# 获取到书各个章节的cid
async def get_info(book_id):
    print("Book ID: " + book_id)
    cid = []
    url = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"' + book_id + '"}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            # 获取到各个章节的信息
            chapters = (await resp.json())["data"]["novel"]["items"]

            for c in chapters:
                # title = c["title"]
                cid.append(c["cid"])
    return cid


# 下载各个章节
async def download(book_id, cid):
    async with aiohttp.ClientSession() as session:
        data = {
            "book_id": book_id,
            "cid": f"{book_id}|{cid}",
            "need_bookinfo": 1
        }
        content_url = f"http://dushu.baidu.com/api/pc/getChapterContent?data={json.dumps(data)}"

        async with session.get(content_url, headers=headers) as content:
            chapter_title = (await content.json())["data"]["novel"]["chapter_title"]
            text = (await content.json())["data"]["novel"]["content"]
            book_title = (await content.json())["data"]["bookinfo"]["book_name"]

            # path = f"../novel/{book_title}"
            async with aiofiles.open(f"{chapter_title}.txt", mode="w", encoding="UTF-8") as f:
                await f.write(text)


async def main():
    # flag 用来记录章节数，也用来记录是否已经判断路径存在，和是否已经清空路径

    res1 = await asyncio.wait([asyncio.create_task(search())])
    book_id = res1[0].pop().result()  # 获取到函数的返回值

    res2 = await asyncio.wait([asyncio.create_task(get_info(book_id))])
    cid_list = res2[0].pop().result()  # 获取到函数的返回值，是个列表

    tasks = []
    for cid in cid_list:
        tasks.append(asyncio.create_task(download(book_id, cid)))

    await asyncio.wait(tasks)
    print("Download Success!")


if __name__ == '__main__':
    asyncio.run(main())
