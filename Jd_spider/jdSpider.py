#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2020/5/18
# @Author  : 圈圈烃
# @File    : jdSpider
# @Description:
#
#
import requests
import csv
import time
from bs4 import BeautifulSoup


def get_html(url):
    """获取页面"""
    headers = {
        "Host": "search.jd.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    resp = requests.get(url, headers=headers, timeout=5)
    resp.encoding = "utf-8"
    return resp.text


def get_comment(id_list):
    """根据ID列表获取评论数据"""
    url = "https://club.jd.com/comment/productCommentSummaries.action"
    headers = {
        "Host": "club.jd.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
    }
    id_str = ","
    id_str = id_str.join(id_list)
    params = {
        "referenceIds": id_str,
        "callback": "",
        "_": "1589772400990",
    }
    resp = requests.get(url, params=params, headers=headers)
    resp.encoding = resp.apparent_encoding
    print(resp.text)
    return resp.json()


def paser_html(html):
    """页面解析"""
    goods_list = []
    goods_id_list = []
    soup = BeautifulSoup(html, "html.parser")
    lis = soup.find_all("li", {"class": "gl-item"})
    for li in lis:
        p_div = li.find("div", {"class": "p-price"})
        n_div = li.find("div", {"class": "p-name"})
        good_id = li["data-sku"]
        good_name = n_div.a.em.get_text()
        good_price = p_div.strong.i.get_text()
        good_url = n_div.a["href"]
        good_list = [good_id, good_name, good_price, good_url]
        goods_list.append(good_list)
        goods_id_list.append(good_id)
    # 异步加载评价
    resp_json = get_comment(goods_id_list)
    comments_list = resp_json["CommentsCount"]
    for i in range(len(goods_list)):
        CommentCount = comments_list[i]["CommentCount"]  # 评价人数
        DefaultGoodCount = comments_list[i]["DefaultGoodCount"]  # 默认好评
        GoodCount = comments_list[i]["GoodCount"]  # 好评
        GeneralCount = comments_list[i]["GeneralCount"]  # 中评
        PoorCount = comments_list[i]["PoorCount"]  # 差评
        GoodRate = comments_list[i]["GoodRate"]  # 好评率
        GeneralRate = comments_list[i]["GeneralRate"]  # 中评率
        PoorRate = comments_list[i]["PoorRate"]  # 差评率
        AfterCount = comments_list[i]["AfterCount"]  # 追评
        VideoCount = comments_list[i]["VideoCount"]  # 视频晒单
        goods_list[i].extend([CommentCount, GoodRate, GeneralRate, PoorRate])
    return goods_list


def main():
    info_list = []
    page_count = 300
    good_type = "口罩"
    start_url = "https://search.jd.com/Search?keyword=" + good_type
    for i in range(page_count):
        try:
            url = start_url + "&page=" + str(i)
            html = get_html(url)
            goods_list = paser_html(html)
            info_list.extend(goods_list)
            # time.sleep(1)
        except Exception as e:
            print(e)
    # 写入csv
    headers = ["商品Id", "商品名称", "商品价格", "商品Url", "评价人数", "好评率", "中评率", "差评率"]
    with open("./jd_goods.csv", "w", newline="", encoding='utf_8_sig') as fw:
        fcsv = csv.writer(fw)
        fcsv.writerow(headers)
        fcsv.writerows(info_list)
        print("(￣▽￣)文件保存成功！")


if __name__ == '__main__':
    main()
