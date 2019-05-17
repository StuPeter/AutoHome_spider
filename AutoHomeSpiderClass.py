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
from AutoHomeFont import get_new_font_dict
import requests
import csv
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
        self.seriesApi = "https://club.autohome.com.cn/frontapi/bbs/getSeriesByLetter?firstLetter=%s"  # 所有车系论坛链接api
        self.forumUrl = "https://club.autohome.com.cn/bbs/forum-c-%d-1.html"
        self.replyUrl = "https://clubajax.autohome.com.cn/topic/rv"

    def get_html(self, url):
        res = requests.get(url, headers=self.headers, timeout=5)
        return res

    def get_reply_view(self, idList):
        """获取某帖子的回复量和访问量"""
        headers = {
            "Host": "clubajax.autohome.com.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        idStr = ""
        idStr = idStr + ",".join(idList)
        params = {
            "ids": idStr
        }
        res = requests.get(self.replyUrl, headers=headers, params=params)
        return res

    def get_bbs_url(self):
        """获取车型论坛链接"""
        res = self.get_html(self.seriesApi % "L")  # 雷克萨斯车系首字母为"L"
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

    def analysis_forumPost(self, res):
        """解析论坛帖子"""
        soup = BeautifulSoup(res.text, 'html.parser')
        postList = soup.find_all('dl', {'class': 'list_dl'})
        topic = dict()
        topic['url'] = list()           # 帖子链接列表
        topic['title'] = list()          # 帖子标题列表
        topic['date'] = list()          # 发帖日期列表
        topic['author'] = list()        # 发帖用户列表
        topic['id'] = list()            # 帖子Id列表
        topic['reply'] = list()    # 帖子回复量列表
        topic['views'] = list()     # 帖子访问量列表
        for post in postList:
            try:
                dt = post.find('a', {'class', 'a_topic'})
                topicUrl = dt['href']        # 帖子链接
                topicTitle = dt.get_text()    # 帖子标题
                topicDate = post.find('span', {'class', 'tdate'}).get_text()                # 发帖日期
                topicAuthor = post.find('a', {'class', 'linkblack'}).get_text()             # 发帖用户
                topicId = post.find('dd', {'class', 'cli_dd'})['lang']                      # 帖子ID
                topic['url'].append(topicUrl)
                topic['title'].append(topicTitle)
                topic['date'].append(topicDate)
                topic['author'].append(topicAuthor)
                topic['id'].append(topicId)
            except Exception as e:
                print(e)
        # 异步获取访问量和回复量
        res = self.get_reply_view(topic['id'])
        for i in range(len(topic['id'])):
            for reply in res.json():
                if str(reply['topicid']) == str(topic['id'][i]):
                    topic['reply'].append(reply['replys'])
                    topic['views'].append(reply['views'])
                    break
        return topic

    def analysis_Post(self, res):
        """解析帖子"""
        ttfUrl = re.findall(',url\(\'//(.*ttf)', res.text)[0]
        ttfRes = requests.get("https://" + ttfUrl)
        with open('temp.ttf', 'wb') as fw:
            fw.write(ttfRes.content)
        print("反爬虫字体 %s 下载成功..." % (ttfUrl.split('/')[-1]))
        standardFontPath = 'standardFont.ttf'
        newFontPath = 'temp.ttf'
        font_dict = get_new_font_dict(standardFontPath, newFontPath)
        print(font_dict)


def main():
    # url = 'https://club.autohome.com.cn/bbs/forum-c-403-2.html'
    url = 'https://club.autohome.com.cn/bbs/thread/3b9d8d1cfd0e9431/80967895-1.html'
    auto = AutoHomeSpider()
    res = auto.get_html(url)
    # topic = auto.analysis_forumPost(res)
    auto.analysis_Post(res)


    # # 写入csv文件
    # headers = ['Id', 'Title', 'Author', 'Reply', 'Views', 'Date', 'Url']
    # rows = list()
    # for i in range(len(topic['id'])):
    #     rows.append((
    #                 topic['id'][i], topic['title'][i], topic['author'][i], topic['reply'][i], topic['views'][i],
    #                 topic['date'][i], "https://club.autohome.com.cn" + topic['url'][i]))
    # with open("test.csv", "a", newline="", encoding='utf_8_sig') as fw:
    #     f_csv = csv.writer(fw)
    #     f_csv.writerow(headers)
    #     f_csv.writerows(rows)
    #     print("CSV文件保存成功！")


if __name__ == '__main__':
    main()
