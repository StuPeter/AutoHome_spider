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
from snownlp import SnowNLP
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
        self.forumApi = "https://club.autohome.com.cn/frontapi/topics/getByBbsId"
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
        idStr = ","
        idStr = idStr.join(idList)
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

    def analysis_forumPost(self, pageindex, bbsid):
        """解析论坛帖子"""
        params = {
            "pageindex": pageindex,
            "pagesize": "50",
            "bbs": "c",
            "bbsid": bbsid,
            "fields": "topicid,title,post_memberid,post_membername,postdate,ispoll,ispic,isrefine,replycount,viewcount,"
                      "videoid,isvideo,videoinfo,qainfo,tags,topictype,imgs,jximgs,url,piccount,isjingxuan,issolve,"
                      "liveid,livecover,topicimgs",
            "orderby": "lastpostdata-",
        }
        res = requests.get(self.forumApi, headers=self.headers, params=params, timeout=5)
        postList = res.json()['result']['list']
        topic = dict()
        topic['url'] = list()  # 帖子链接列表
        topic['title'] = list()  # 帖子标题列表
        topic['date'] = list()  # 发帖日期列表
        topic['author'] = list()  # 发帖用户列表
        topic['id'] = list()  # 帖子Id列表
        topic['reply'] = list()  # 帖子回复量列表
        topic['views'] = list()  # 帖子访问量列表
        for post in postList:
            topic['url'].append(post['url'])
            topic['title'].append(post['title'])
            topic['date'].append(post['postdate'])
            topic['author'].append(post['post_membername'])
            topic['id'].append(str(post['topicid']))
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
        """解析帖子内容"""
        # 解析帖子中的字体文件
        ttfUrl = re.findall(',url\(\'//(.*ttf)', res.text)[0]
        ttfRes = requests.get("https://" + ttfUrl)
        with open('temp.ttf', 'wb') as fw:
            fw.write(ttfRes.content)
        print("反爬虫字体 %s 下载成功..." % (ttfUrl.split('/')[-1]))
        standardFontPath = 'standardFont.ttf'
        newFontPath = 'temp.ttf'
        font_dict = get_new_font_dict(standardFontPath, newFontPath)
        # print(font_dict)
        # 解析帖子中的数据
        soup = BeautifulSoup(res.text, 'html.parser')
        post = dict()
        post['userName'] = list()  # 用户名
        post['excellent'] = list()  # 精华帖
        post['postNumber'] = list()  # 发帖量
        post['replyNumber'] = list()  # 回复量
        post['loginDate'] = list()  # 注册时间
        post['location'] = list()  # 地区
        post['postTime'] = list()  # 回复时间
        post['postContent'] = list()  # 回复内容
        post['postSentiments'] = list()  # 回复内容积极程度0~1，1为积极
        replyList = soup.find_all('div', {'class': 'clearfix contstxt outer-section', 'style': ''})
        for reply in replyList:
            userName = reply.find('li', {'class': 'txtcenter fw'}).a.get_text().replace(" ", "").replace("\r\n", "")
            ul = reply.find('ul', {'class': 'leftlist'})
            liList = ul.find_all('li')
            excellent = liList[2].get_text().replace(" ", "").replace("\n", "").replace("精华：", "").replace("帖",
                                                                                                           "").replace(
                "\r", "")
            postNumber, replyNumber = liList[3].get_text().replace(" ", "").replace("\n", "").replace("帖子：",
                                                                                                      "").replace("回",
                                                                                                                  "").replace(
                "帖", "").replace("\xa0", "").split("|")
            loginDate = liList[4].get_text().replace(" ", "").replace("\n", "").replace("注册：", "")
            location = liList[5].get_text().replace(" ", "").replace("\n", "").replace("来自：", "")
            postTime = reply.find('span', {'xname': 'date'}).get_text()
            postReply = reply.find('div', {'class': 'w740'})
            # 解析反爬虫字体
            yy_reply = reply.find('div', {'class': 'yy_reply_cont'})
            if yy_reply:
                content = yy_reply.get_text().encode('unicode_escape')
            else:
                content = postReply.get_text().encode('unicode_escape')
            for key, value in font_dict.items():
                new_key = r"\u" + key[3:].lower()
                content = content.replace(str.encode(new_key), str.encode(value))
            postContent = content.decode('unicode_escape').replace(" ", "").replace("\n", "").replace("\xa0", "")
            # print(postContent)
            # print(10*"=")
            # 组合数据
            post['userName'].append(userName)
            post['excellent'].append(excellent)
            post['postNumber'].append(postNumber)
            post['replyNumber'].append(replyNumber)
            post['loginDate'].append(loginDate)
            post['location'].append(location)
            post['postTime'].append(postTime)
            post['postContent'].append(postContent)
            # 自然语言处理-情感分析
            try:
                s = SnowNLP(postContent)
                score = s.sentiments
            except:
                score = "None"
            post['postSentiments'].append(score)
        return post

    def write_csv(self, writeType, contentDict):
        """写入csv文件"""
        if writeType == "topic":
            topic = contentDict
            # headers = ['Id', 'Title', 'Author', 'Reply', 'Views', 'Date', 'Url']
            rows = list()
            for i in range(len(topic['id'])):
                rows.append((
                    topic['id'][i], topic['title'][i], topic['author'][i], topic['reply'][i], topic['views'][i],
                    topic['date'][i], "https://club.autohome.com.cn" + topic['url'][i]))
            with open("topic.csv", "a", newline="", encoding='utf_8_sig') as fw:
                f_csv = csv.writer(fw)
                # f_csv.writerow(headers)
                f_csv.writerows(rows)
                print("CSV文件保存成功！")
        else:
            post = contentDict
            # headers = ['用户名', '精华帖数量', '发帖量', '回帖量', '注册日期', '地理位置', '回复日期', '回复内容', '情感得分']
            rows = list()
            for i in range(len(post['userName'])):
                rows.append((
                    post['userName'][i], post['excellent'][i], post['postNumber'][i], post['replyNumber'][i],
                    post['loginDate'][i], post['location'][i], post['postTime'][i], post['postContent'][i],
                    post['postSentiments'][i]))
            with open("post.csv", "a", newline="", encoding='utf_8_sig') as fw:
                f_csv = csv.writer(fw)
                # f_csv.writerow(headers)
                f_csv.writerows(rows)
                print("CSV文件保存成功！")


def main():
    url = 'https://club.autohome.com.cn/bbs/forum-c-403-1.html'
    auto = AutoHomeSpider()
    # res = auto.get_html(url)
    topic = auto.analysis_forumPost(pageindex=1, bbsid=403)
    print(topic)
    # for postUrl in topic['url']:
    #     print(postUrl)


    # soup = BeautifulSoup(res.text, 'html.parser')
    # page = int(soup.find('span', {'class': 'fs'})['title'][2])
    # for i in range(page):
    #     postUrl = 'https://club.autohome.com.cn/bbs/thread/788b1cc73317fd0d/80766349-1.html'.replace('-1',
    #                                                                                                  '-' + str(i + 1))
    #     print(postUrl)
    #     res = auto.get_html(postUrl)
    #     post = auto.analysis_Post(res)
    #     auto.write_csv(writeType='post', contentDict=post)




if __name__ == '__main__':
    main()
