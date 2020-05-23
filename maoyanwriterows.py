"""
抓取猫眼top100,减少本地磁盘IO提升数据处理效率
"""

import re, requests, time, random,csv


class MaoYanSpider:
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        self.headers = {'Accept-Encoding':'gzip, deflate, br','Upgrade-Insecure-Requests': '1','User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        # 计数
        self.i = 0
        self.f = open('maoyan_all.csv','a')
        self.writer = csv.writer(self.f)
        #存储所有电影信息的列表 用于最后一次性写入
        self.all_film_list = []

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
        item = {}
        for i in r_list:
            t = (
                i[0].strip(),
                i[1].strip()[3:],
                i[2].strip()[5:]
            )
            #添加到列表中
            self.all_film_list.append(t)
            print(t)



    def run(self):
        for i in range(0,91,10):
            url = self.url.format(i)
            self.get_html(url)
            #控制爬取的速度uniform随机浮点数
            time.sleep(random.uniform(0,2))
        #写入数据,使用writerows
        self.writer.writerows(self.all_film_list)
        self.f.close()

if __name__ == '__main__':
    spider = MaoYanSpider()
    spider.run()