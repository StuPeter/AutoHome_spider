#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/11/18
# @Author  : 圈圈烃
# @File    : main
# @Description:
#
#
from AutoHomeSpiderClass import AutoHomeSpider
from bs4 import BeautifulSoup
import time


def updateCarUrl(Car=""):
    auto = AutoHomeSpider()
    auto.get_bbs_url(Car)


def main(pageIndex, BBSId):
    """
    :param pageIndex: 页码，默认只爬取第一页
    :param BBSId:获取BBSID为352
    :return:
    """
    # 创建汽车之家爬虫类
    auto = AutoHomeSpider(nlp=True)
    # 选定论坛页，其中pageindex表示页码，bbsid表示车型代码
    topic = auto.analysis_forumPost(pageindex=pageIndex, bbsid=BBSId)
    # 循环爬取该页所有帖子
    for postUrl in topic['url']:
        res = auto.get_html(postUrl)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            page = int(soup.find('span', {'class': 'fs'})['title'][2])
        except:
            page = 1
        # 循环爬取该帖子所有回复
        for i in range(page):
            time.sleep(2)  # 延时设定为2秒，太快会出现验证码导致爬取失败
            newPostUrl = postUrl.replace('-1', '-' + str(i + 1))
            print(newPostUrl)
            res = auto.get_html(newPostUrl)
            try:
                post = auto.analysis_Post(res)
                print(post)
                auto.write_csv(contentDict=post, bbsid=BBSId)  # 保存为csv文件
            except Exception as e:
                print(e)


if __name__ == '__main__':
    # 更新targetCarUrl.txt
    # updateCarUrl()
    # 爬虫主程序
    main(pageIndex=1, BBSId=3411)
