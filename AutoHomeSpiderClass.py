#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/5/5
# @Author  : 圈圈烃
# @File    : AutoHomeSpiderClass
# @Description:
#
#
from bs4 import BeautifulSoup
import requests
import re
import random


class AutoHomeSpider:

    def __init__(self):
        self.headers = {
            "Host": "club.autohome.com.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            # "Referer": "https://club.autohome.com.cn/bbs/forum-c-871-1.html",
            "Connection": "keep-alive",
            # "Cookie": "ahpvno=6; pvidchain=3311253,3311253,6826793; fvlid=1557020630617i73BVtciYK; sessionip=183.132.184.132; sessionid=B6D727B8-56B0-46DD-9140-B514F3B80337%7C%7C2019-05-05+09%3A43%3A50.886%7C%7C0; autoid=a0a8f7d79866d31f24be9bcf9724c23c; ref=0%7C0%7C0%7C0%7C2019-05-05+09%3A58%3A43.321%7C2019-05-05+09%3A43%3A50.886; sessionvid=6BE01EFE-8AC0-4E09-95CA-4E2E9BC9EE5B; area=330299; ahpau=1; csrfToken=VGKFGgbqfyaZYv04pi7q1A3U; historybbsName4=c-871%7C%E9%AB%98%E5%B0%94%E5%A4%AB; __ah_uuid_ng=u_76903609; ahrlid=1557020956401U1ZVKhrjn6-1557022506437",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }
        self.seriesApi = "https://club.autohome.com.cn/frontapi/bbs/getSeriesByLetter?firstLetter=%s"     # 所有车系论坛链接api
        self.forumUrl = "https://club.autohome.com.cn/bbs/forum-c-%d-1.html"

    def get_html(self, url):
        res = requests.get(url, headers=self.headers, timeout=5)
        return res

    def get_bbs_url(self):
        """获取车型论坛链接"""
        res = self.get_html(self.seriesApi % "L")   # 雷克萨斯车系首字母为"L"
        allCarId = res.json()['result'][0]['bbsBrand']
        for i in range(len(allCarId)):
            if allCarId[i]['bbsBrandName'] == "雷克萨斯":
                indexCarId = i
                break
        try:
            for targetCar in allCarId[indexCarId]['bbsList']:
                targetCarUrl = self.forumUrl % (targetCar['bbsId'])
                targetCarName = targetCar['bbsName']
                with open('targetCarUrl.txt', 'a', encoding='utf-8') as fw:
                    fw.write(targetCarName + "||" + targetCarUrl + "\n")
            print("目标车型链接文本保存成功...")
        except Exception as e:
            print(e)

    def analysis_forumList(self, res):
        """解析论坛帖子"""
        soup = BeautifulSoup(res, 'html.parser')
        urlList = soup.find_all('div', {'id': 'js-alphabet-bbs-wrap'})


def main():
    url = 'https://club.autohome.com.cn/#pvareaid=3311253'
    auto = AutoHomeSpider()
    res = auto.get_html(url)
    auto.get_bbs_url()


if __name__ == '__main__':
    main()
