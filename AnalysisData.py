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


def map_visualmap(dataP, dataN) -> Map:
    c = (
        Map()
            .add("雷克萨斯IS好评分布", dataP, "china")
            .add("雷克萨斯IS差评分布", dataN, "china")
            .set_global_opts(
            # title_opts=opts.TitleOpts(title="雷克萨斯IS好评分布图"),
            # title_opts=opts.TitleOpts(title="雷克萨斯IS差评分布图"),
            # title_opts=opts.TitleOpts(title="雷克萨斯IS车友分布图"),
            visualmap_opts=opts.VisualMapOpts(max_=200),
        )
    )
    return c


def bar_base(data) -> Bar:
    c = (
        Bar()
            .add_xaxis(['好评指数', '差评指数'])
            .add_yaxis("雷克萨斯ES", data)
            .set_global_opts(title_opts=opts.TitleOpts(title="雷克萨斯IS情感分析", subtitle="好差评指数"))
    )
    return c


def main():
    userLocList = list()
    locList = list()
    scoreList = list()
    emotionalList = list()
    csvData = csv.reader(open('雷克萨斯IS.csv', encoding='utf_8_sig'))
    for row in csvData:
        userLoc = row[0] + "|" + row[5][:2]
        if row[8] != 'None':
            score = round(float(row[8]), 5)
            scoreList.append(score)
            if score >= 0.5:
                emotionalList.append(1)
                # userLocList.append(userLoc)  # 好评
            else:
                emotionalList.append(0)
                userLocList.append(userLoc) # 差评
        # userLocList.append(userLoc) # 分布
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
    P = [('湖北', 15), ('新疆', 1), ('河南', 5), ('广西', 19), ('青海', 2), ('山西', 2), ('陕西', 5), ('吉林', 1), ('辽宁', 11), ('广东', 176), ('上海', 38), ('贵州', 10), ('澳门', 3), ('湖南', 7), ('浙江', 82), ('天津', 7), ('河北', 11), ('海外', 3), ('重庆', 7), ('四川', 35), ('安徽', 13), ('江苏', 73), ('北京', 55), ('内蒙古', 3), ('黑龙', 4), ('云南', 11), ('其它', 2), ('福建', 21), ('西藏', 3), ('江西', 7), ('山东', 24), ('海南', 4), ('甘肃', 1)]
    N = [('广东', 131), ('江苏', 67), ('福建', 10), ('海外', 2), ('安徽', 5), ('上海', 36), ('黑龙', 3), ('西藏', 1), ('新疆', 2), ('河南', 6), ('湖北', 10), ('吉林', 1), ('重庆', 7), ('云南', 12), ('湖南', 8), ('贵州', 6), ('甘肃', 2), ('天津', 5), ('广西', 14), ('山西', 3), ('江西', 5), ('河北', 9), ('陕西', 10), ('北京', 46), ('澳门', 3), ('辽宁', 8), ('香港', 4), ('四川', 32), ('山东', 16), ('浙江', 42), ('内蒙古', 1), ('海南', 1)]
    # 绘制分布图
    c = map_visualmap(P, N)
    c.render()
    # 绘制直方图
    # c2 = bar_base([emotionalList.count(1), emotionalList.count(0)])
    # c2.render()


if __name__ == '__main__':
    main()
