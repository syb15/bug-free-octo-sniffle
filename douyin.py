#导入自动化模块
from DrissionPage import ChromiumPage
#导入时间模块
import datetime
#导入csv
import csv
#创建文件对象
f = open('dy.csv', mode='w', encoding='utf-8-sig', newline='')
#字典写入方法
csv_writer = csv.DictWriter(f,fieldnames=['昵称','地区','时间','评论'])
#写入标头
csv_writer.writeheader()
#打开浏览器
driver = ChromiumPage()
#监听数据包
driver.listen.start('aweme/v1/web/comment/list/')
#访问网站
driver.get('https://www.douyin.com/video/7353500880198536457')
for page in range(15):
    print(f'正在采集{page+1}页的数据')
    #下滑到页面底部
    driver.scroll.to_bottom()
    #等待数据包加载
    resp = driver.listen.wait()
    #直接获取数据包返回的响应数据
    json_data = resp.response.body
    #解析数据，提取评论
    comments = json_data['comments']
    #for循环遍历，提取相关内容
    for index in comments:
        #键值对取值，提取内容
        text = index['text']#评论内容
        nickname = index['user']['nickname']#昵称
        create_time = index['create_time']#评论时间戳
        #时间戳转为日期
        date = str(datetime.datetime.fromtimestamp(create_time))
        ip_label = index['ip_label']#地区
        #将数据放入字典
        dit = {
            '昵称': nickname,
            '地区': ip_label,
            '时间': date,
            '评论': text,
        }
        #写入数据
        csv_writer.writerow(dit)
        print(dit)