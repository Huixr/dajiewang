import threading

import requests
import json
from lxml import etree
import MySQLdb
conn = MySQLdb.connect(
            host='localhost',  # mysql所在主机的ip
            port=3306,  # mysql的端口号
            user="root",  # mysql 用户名
            password="123456",  # mysql 的密码
            db="snick",  # 要使用的库名
            charset="utf8"  # 连接中使用的字符集
        )
cursor=conn.cursor()
headers = {
    'referer': 'https://so.dajie.com/job',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
}


def get_url():

    page_num=50
    while True:
        try:
            session = requests.Session()
            session.get(url='https://so.dajie.com/job', headers=headers)
            res = session.get(url = 'https://job.dajie.com/qz1-p'+str(page_num)+'/',headers=headers).content.decode()
            page_num += 1
            print(page_num)
            ele = etree.HTML(res)
            eles = ele.xpath('//div[@class="boxCenter"]/p/a/@href')
        except:
            continue
        for i in eles:
            # print(i)
            if i !='':
                res1 = session.get(url=i,headers=headers).content.decode()
                ele1 = etree.HTML(res1)
                try:
                    name = ele1.xpath('//span[@class="job-name"]/text()')[0].strip()
                except:
                    name=''
                try:
                    salary = ele1.xpath('//span[@class="job-money"]/em/text()')[0].strip()
                except:
                    salary=''
                try:
                    full_time =ele1.xpath('//div[@class="job-msg-center"]/ul/li/span/text()')[0].strip()
                except:
                    full_time=''
                try:
                    city =ele1.xpath('//div[@class="job-msg-center"]/ul/li/span/text()')[1].strip()
                except:
                    city=''
                try:
                    num =ele1.xpath('//div[@class="job-msg-center"]/ul/li/span/text()')[2].strip()
                except:
                    num=''
                try:
                    exp =ele1.xpath('//div[@class="job-msg-center"]/ul/li/span/text()')[3].strip()
                except:
                    exp=''
                try :
                    educational =ele1.xpath('//div[@class="job-msg-center"]/ul/li/span/text()')[4].strip()
                except:
                    educational=''
                try:
                    conpy =ele1.xpath('//p[@class="compang-msg"]/span/text()')[0].strip()
                except:
                    conpy=''
                try:
                    add = ele1.xpath('//p[@class="compang-msg"]/span/text()')[1].strip()
                except:
                    add=''
                try:
                    tel =ele1.xpath('//p[@class="compang-msg"]/span/text()')[2].strip()
                except:
                    tel=''
                print(name, salary, full_time, city, num, exp, educational)

                sql = 'insert into dajie(name,salary,full_time,city,num,exp,educational,conpy,address,tel) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql,(name,salary,full_time,city,num,exp,educational,conpy,add,tel))
                conn.commit()



if __name__ == '__main__':
    get_url()
    # for i in range(10):
    #     threading.Thread(target=get_url()).start()
    cursor.close()
    conn.close()

















