import requests
import time

url = 'https://nco.zjgsu.edu.cn/genqrcode/2019032'

# file = open("C:/Users/Administrator/Desktop/python文件/spide/helloSpide.txt", "r")

# file_read = file.readlines()  # 读取文件内容（以列表形式）
# lenthOfFile = len(file_read)  # 确定长度
# for i in range(0, lenthOfFile, 4):  # 这里是4后边增加了邮箱信息之后会变成5
for i in range(0, 1, 4):
    # 每一个for循环签到一次
    # file_read_name = file_read[i]  # 读取用户名（学号）
    file_read_name = "2037020134"
    file_read_name = file_read_name.strip()  # 将读取的用户名去空格及回车
    # file_read_pass = file_read[i + 1]  # 读取密码
    file_read_pass = "HAOhao020711/"
    file_read_pass = file_read_pass.strip()
    # file_read_first_location = file_read[i + 2]  # 读取省市
    file_read_first_location = "浙江"
    file_read_first_location = file_read_first_location.strip()
    # file_read_last_location = file_read[i + 3]  # 读取地区
    file_read_last_location = "杭州"
    file_read_last_location = file_read_last_location.strip()
    # 读取文件内容并存储
    # 以下是第一个界面
    myHeaders_1 = {
        'User-Agent': 'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02 '
        # 页面只允许手机端访问于是更改头部为手机可以直接网上搜代理（这一步很关键）
    }
    url = 'https://nco.zjgsu.edu.cn/genqrcode/2019032'
    # 向https://nco.zjgsu.edu.cn/genqrcode/2019032发送请求(进入登录界面)
    r3 = requests.post(url, headers=myHeaders_1)

    yourLocal1 = file_read_first_location  # 读取现在地址的首地址（例如浙江省杭州市）
    yourLocal2 = file_read_last_location  # 读取具体地址
    myHeaders_2 = {
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'zjgsusessionsid=s%3AGSYaaVwF_2pedsizsHYTYSY64hVl3vL_.NMnLf1bV1PJSAS%2FeZXUkcyPkFpBq%2BcMVQYq4XPHXAAU; _ncov_uuid=a59e0ac8-da06-4fb1-83d8-000976c317a9; _ncov_username=1910080117; _ncov_psswd=09187X',
        'User-Agent': 'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02 '

    }
    # 将获得的cookie传到下一个文件头（进行cookie的替换）
    myHeaders_2['Cookie'] = r3.headers['set-cookie']
    payload = {
        'name': ' ', 'psswd': ' '
    }
    payload['name'] = file_read_name  # 设置post参数
    payload['psswd'] = file_read_pass  # 设置post参数
    url = 'https://nco.zjgsu.edu.cn/login'
    r = requests.post(url, data=payload, headers=myHeaders_2)  # 登录
    # r.encoding='utf-8'
    print(r.text)
    print(r.headers)
    time.sleep(10)  # 界面跳转休息十秒怕被抓

    myHeaders_3 = {
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'zjgsusessionsid=s%3AOIlBmUda3tnT-fWds6uWEKKADgTt3IAd.zQ1LcseRzDNFPv5EU1AlkyyWeSMz6424x6HK8cbov8Q; _ncov_uuid=03d31c9b-696f-4429-a0ca-6e2b7a2e10ce; _ncov_username=1910080117; _ncov_psswd=09187X',
        'User-Agent': 'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02 '

    }
    myHeaders_3['Cookie'] = r.headers['set-cookie']  # 传递cookie
    payload2 = {
        'uuid': 'a59e0ac8-da06-4fb1-83d8-000976c317a9',
        'locationInfo': '%E6%B5%99%E6%B1%9F%E7%9C%81%E6%9D%AD%E5%B7%9E%E5%B8%82',
        'currentResd': '%E6%B5%99%E6%B1%9F%E7%9C%81%E6%B8%A9%E5%B7%9E%E5%B8%82%E9%BE%99%E6%B8%AF%E5%B8%82%E4%B8%B4%E6%B8%AF%E8%B7%AF862%E5%8F%B7',
        'fromHbToZjDate': '',
        'fromHbToZj': 'C',
        'fromWtToHzDate': '',
        'fromWtToHz': 'B',
        'meetDate': '',
        'meetCase': 'C',
        'travelDate': '',
        'travelCase': 'D',
        'medObsvReason': '',
        'medObsv': 'B',
        'belowCaseDesc': '',
        'belowCase': 'D',
        'temperature': '',
        'notApplyReason': '',
        'hzQRCode': 'A',
        'specialDesc': ''
    }
    payload2['locationInfo'] = yourLocal1  # 换地址
    payload2['currentResd'] = yourLocal2  # 换地址
    url2 = 'https://nco.zjgsu.edu.cn/'
    r2 = requests.post(url2, data=payload2, headers=myHeaders_2)  # 打卡成功
    # r.encoding='utf-8'
    print(r2.text)
    time.sleep(5)  # 完成一个人的休眠五秒然后继续打卡下一个人
