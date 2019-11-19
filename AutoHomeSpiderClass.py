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


class AutoHomeSpider:

    def __init__(self, nlp=False):
        """
        :param nlp: 是否开启评论情感打分功能，默认False，如果是True的话，需要安装snownlp。
        """
        self.headers = {
            "Host": "club.autohome.com.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            # "Referer": "https://club.autohome.com.cn/bbs/forum-c-871-1.html",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }
        self.seriesApi = "https://club.autohome.com.cn/frontapi/bbs/getSeriesByLetter?firstLetter=%s"  # 所有车系论坛链接api
        self.forumApi = "https://club.autohome.com.cn/frontapi/topics/getByBbsId"
        self.forumUrl = "https://club.autohome.com.cn/bbs/forum-c-%d-1.html"
        self.replyUrl = "https://clubajax.autohome.com.cn/topic/rv"
        self.nlp = nlp
        self.ttfPath = "TTF/temp.ttf"
        self.standardTTFPath = "TTF/standardFont.ttf"

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

    def get_bbs_url(self, bbsBrandName=""):
        """
        获取车型论坛链接
        :param bbsBrandName: 品牌名，例如宝马，奔驰等，默认空的话就获取所有车。
        :return:
        """
        contentList = ["车型 || BBSId || 车型论坛链接\n"]
        res = self.get_html(self.seriesApi)
        allCars = res.json()['result']
        for Car in allCars:
            for bbsBrand in Car["bbsBrand"]:
                for bbsList in bbsBrand["bbsList"]:
                    targetCarBBSId = bbsList['bbsId']
                    targetCarUrl = self.forumUrl % (bbsList['bbsId'])
                    targetCarName = bbsList['bbsName']
                    if bbsBrandName != "":
                        if bbsBrandName in targetCarName:
                            contentList.append(
                                targetCarName + " || " + str(targetCarBBSId) + " || " + targetCarUrl + "\n")
                    else:
                        contentList.append(targetCarName + " || " + str(targetCarBBSId) + " || " + targetCarUrl + "\n")
        with open('targetCarUrl.txt', 'w', encoding='utf-8') as fw:
            for s in contentList:
                fw.write(s)
        print(bbsBrandName + "所有车型链接保存成功...")

    def analysis_forumPost(self, pageindex, bbsid):
        """
        解析论坛帖子
        :param pageindex: 页码
        :param bbsid: 车型ID
        :return:
        """
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
        """
        解析帖子内容
        :param res: html
        :return:
        """
        # 解析帖子中的字体文件
        ttfUrl = re.findall(',url\(\'//(.*ttf)', res.text)[0]
        ttfRes = requests.get("https://" + ttfUrl)
        with open(self.ttfPath, 'wb') as fw:
            fw.write(ttfRes.content)
        print("反爬虫字体 %s 下载成功..." % (ttfUrl.split('/')[-1]))
        standardFontPath = self.standardTTFPath
        newFontPath = self.ttfPath
        font_dict = get_new_font_dict(standardFontPath, newFontPath)
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
        replyList = soup.find_all('div', {'class': 'clearfix contstxt outer-section', 'style': ''})
        for reply in replyList:
            userName = reply.find('li', {'class': 'txtcenter fw'}).a.get_text().replace(" ", "").replace("\r\n", "")
            ul = reply.find('ul', {'class': 'leftlist'})
            liList = ul.find_all('li')
            excellent = liList[2].get_text().replace(" ", "").replace("\n", "").replace("精华：", "").replace("帖", ""). \
                replace("\r", "")
            postNumber, replyNumber = liList[3].get_text().replace(" ", "").replace("\n", "").replace("帖子：", ""). \
                replace("回", "").replace("帖", "").replace("\xa0", "").split("|")
            loginDate = liList[4].get_text().replace(" ", "").replace("\n", "").replace("注册：", "")
            try:
                location = liList[5].get_text().replace(" ", "").replace("\n", "").replace("来自：", "")
            except:
                location = ""
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
            if self.nlp:
                post['postSentiments'] = list()  # 回复内容积极程度0~1，1为积极
                try:
                    s = SnowNLP(postContent)
                    score = s.sentiments
                except:
                    score = "None"
                post['postSentiments'].append(score)
        return post

    def write_csv(self, contentDict, bbsid, writeType=""):
        """
        写入csv文件
        :param contentDict:
        :param writeType: 数据类型，默认写入analysis_Post函数返回值，如果填写为topic，可以写入analysis_forumPost函数返回。
        :return:
        """
        if writeType == "topic":
            topic = contentDict
            # headers = ['Id', 'Title', 'Author', 'Reply', 'Views', 'Date', 'Url']
            rows = list()
            for i in range(len(topic['id'])):
                rows.append((
                    topic['id'][i], topic['title'][i], topic['author'][i], topic['reply'][i], topic['views'][i],
                    topic['date'][i], "https://club.autohome.com.cn" + topic['url'][i]))
            with open(str(bbsid) + "_topic.csv", "a", newline="", encoding='utf_8_sig') as fw:
                f_csv = csv.writer(fw)
                # f_csv.writerow(headers)
                f_csv.writerows(rows)
                print("CSV文件保存成功！")
        else:
            post = contentDict
            # headers = ['用户名', '精华帖数量', '发帖量', '回帖量', '注册日期', '地理位置', '回复日期', '回复内容', '情感得分']
            rows = list()
            for i in range(len(post['userName'])):
                if self.nlp:
                    rows.append((
                        post['userName'][i], post['excellent'][i], post['postNumber'][i], post['replyNumber'][i],
                        post['loginDate'][i], post['location'][i], post['postTime'][i], post['postContent'][i],
                        post['postSentiments'][i]))
                else:
                    rows.append((
                        post['userName'][i], post['excellent'][i], post['postNumber'][i], post['replyNumber'][i],
                        post['loginDate'][i], post['location'][i], post['postTime'][i], post['postContent'][i]))
            with open(str(bbsid) + "_post.csv", "a", newline="", encoding='utf_8_sig') as fw:
                f_csv = csv.writer(fw)
                # f_csv.writerow(headers)
                try:
                    f_csv.writerows(rows)
                    print("CSV文件保存成功！")
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    auto = AutoHomeSpider()
    res = auto.get_html("https://club.autohome.com.cn/bbs/thread/aa8f44ef6911eb14/84890467-1.html")
    post = auto.analysis_Post(res)
