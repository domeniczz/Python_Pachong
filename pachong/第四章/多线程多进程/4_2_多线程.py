# 线程, 进程
# 进程是资源单位, 每一个进程至少要有一个线程
# 线程是执行单位

# 启动每一个程序默认都会有一个主线程
from threading import Thread  # 线程类


def func():
    for i in range(10):
        print("func", i)


if __name__ == '__main__':
    func()
    for i in range(1000):
        print("main", i)


#  多线程

def func():
    for i in range(10):
        print("func", i)


if __name__ == '__main__':
    t = Thread(target=func)  # 创建线程并给线程安排任务
    t.start()  # 多线程状态为可以开始工作状态, 具体的执行时间由CPU决定

    for i in range(10):
        print("main", i)


# 多线程 类
class MyThread(Thread):  #
    def run(self):  # 固定的    -> 当线程被执行的时候, 被执行的就是run()
        for i in range(10):
            print("子线程", i)


if __name__ == '__main__':
    t = MyThread()
    # t.run()  # 方法的调用了. -> 单线程????
    t.start()  # 开启线程

    for i in range(10):
        print("主线程", i)


#  多线程 传参
def func(name):
    for i in range(10):
        print(name, i)


if __name__ == '__main__':
    t = Thread(target=func, args=("周杰伦", ))  # 创建线程并给线程安排任务，传入的参数是元组，所以“周杰伦”后面要加逗号
    t.start()  # 多线程状态为可以开始工作状态, 具体的执行时间由CPU决定

    for i in range(10):
        print("main", i)


# 多线程 传参
class MyThread(Thread):  #
    def __init__(self, name=None):
        Thread.__init__(self, name=None)
        self.name = name

    def run(self):  # 固定的    -> 当线程被执行的时候, 被执行的就是run()
        for i in range(10):
            print(self.name, i)


if __name__ == '__main__':
    t = MyThread(name="周杰伦")
    # t.run()  # 这就是方法的调用了. -> 单线程
    t.start()  # 开启线程

    for i in range(10):
        print("主线程", i)
