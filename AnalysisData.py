#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/7/8
# @Author  : 圈圈烃
# @File    : AnalysisData
# @Description:汽车之家数据分析
#
#
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Bar
import csv

provinceList = [
    '北京', '广东', '山东', '江苏', '河南', '上海', '河北', '浙江', '香港特别行政区', '陕西', '湖南', '重庆', '福建', '天津', '云南', '四川', '广西壮族自治区',
    '安徽', '海南', '江西', '湖北', '山西', '辽宁', '台湾', '黑龙江', '内蒙古自治区', '澳门特别行政区', '贵州', '甘肃', '青海', '新疆维吾尔自治区', '西藏自治区', '吉林',
    '宁夏回族自治区']


def map_visualmap(data) -> Map:
    c = (
        Map()
            .add("雷克萨斯ES车友分布", data, "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="雷克萨斯ES车友分布"),
            visualmap_opts=opts.VisualMapOpts(max_=200),
        )
    )
    return c


def bar_base(data) -> Bar:
    c = (
        Bar()
            .add_xaxis(['好评指数', '差评指数'])
            .add_yaxis("雷克萨斯ES", data)
            .set_global_opts(title_opts=opts.TitleOpts(title="雷克萨斯ES情感分析", subtitle="好差评指数"))
    )
    return c


def main():
    userLocList = list()
    locList = list()
    scoreList = list()
    emotionalList = list()
    csvData = csv.reader(open('post.csv', encoding='utf_8_sig'))
    for row in csvData:
        userLoc = row[0] + "|" + row[5][:2]
        if row[8] != 'None':
            score = round(float(row[8]), 5)
            scoreList.append(score)
            if score >= 0.5:
                emotionalList.append(1)
            else:
                emotionalList.append(0)
        userLocList.append(userLoc)
    # 根据用户名列表去重
    userLocList = list(set(userLocList))
    # 地理位置统计
    for loc in userLocList:
        loc = loc[-2:]
        if loc == "内蒙":
            loc = "内蒙古"
        locList.append(loc)
    locDict = {}
    locFreqList = list()
    for i in set(locList):
        locDict[i] = locList.count(i)
        locFreq = (i, locList.count(i))
        locFreqList.append(locFreq)
    print(locFreqList)
    # 绘制分布图
    c = map_visualmap(locFreqList)
    # 绘制直方图
    c2 = bar_base([emotionalList.count(1), emotionalList.count(0)])
    c2.render()


if __name__ == '__main__':
    main()
