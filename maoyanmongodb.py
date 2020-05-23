"""
抓取猫眼top100
"""

import re, requests, time, random,csv,pymongo


class MaoYanSpider:
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        self.headers = {'Accept-Encoding':'gzip, deflate, br','Upgrade-Insecure-Requests': '1','User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        # 计数
        self.conn = pymongo.MongoClient(host='localhost',port=27017)
        self.db = self.conn['maoyandb']
        self.set = self.db['maoyanset']

    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).text
        #直接调用解析函数
        self.parse_html(html)

    def parse_html(self,html):
        regex = '<div class="movie-item-info">.*?title="(.*?)".*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>.*?</div>'
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)
        self.save_html(r_list)

    def save_html(self,r_list):
        i_list = []
        for i in r_list:
            # item={}要定义到内部 防止id冲突
            item = {}
            item['name']= i[0].strip(),
            item['star']= i[1].strip(),
            item['time']= i[2].strip()
            i_list.append(item)
            print(item)
        self.set.insert_many(i_list)

    def run(self):
        for i in range(0,91,10):
            url = self.url.format(i)
            self.get_html(url)
            #控制爬取的速度uniform随机浮点数
            time.sleep(random.uniform(0,2))


if __name__ == '__main__':
    spider = MaoYanSpider()
    spider.run()