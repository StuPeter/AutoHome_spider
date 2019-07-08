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
from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Map
import csv

provinceList = [
    '北京', '广东', '山东', '江苏', '河南', '上海', '河北', '浙江', '香港特别行政区', '陕西', '湖南', '重庆', '福建', '天津', '云南', '四川', '广西壮族自治区',
    '安徽', '海南', '江西', '湖北', '山西', '辽宁', '台湾', '黑龙江', '内蒙古自治区', '澳门特别行政区', '贵州', '甘肃', '青海', '新疆维吾尔自治区', '西藏自治区', '吉林',
    '宁夏回族自治区']


def map_visualmap(data) -> Map:
    c = (
        Map()
            .add("商家A", data, "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-VisualMap（分段型）"),
            visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True),
        )
    )
    return c


def main():
    userLocList = list()
    locList = list()
    csvData = csv.reader(open('post.csv', encoding='utf_8_sig'))
    for row in csvData:
        userLoc = row[0] + "|" + row[5][:2]
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
    # print(locDict)
    print(locFreqList)
    c = map_visualmap(locFreqList)
    c.render()

if __name__ == '__main__':
    main()

