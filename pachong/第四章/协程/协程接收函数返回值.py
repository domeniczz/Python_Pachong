import asyncio
import time


async def test1():
    list1 = []
    for i in range(10):
        await asyncio.sleep(3)
        # print(i,"test1")
        list1.append(i)
    return list1


async def test2():
    lit2 = []
    for i in range(15):
        await asyncio.sleep(2)
        # print(i,"test2")
        lit2.append(i)
    return lit2


def run():
    start_time = time.time()

    loop = asyncio.get_event_loop()
    task = loop.create_task(test1())
    task1 = loop.create_task(test2())

    loop.run_until_complete(task)
    loop.run_until_complete(task1)
    loop.close()
    print(task.result())
    print(task1.result())

    end_time = time.time()
    print(end_time - start_time)


run()

'''
输出：
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
30.16243577003479
'''
