#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2020/5/30
# @Author  : 圈圈烃
# @File    : goods_analysis
# @Description:
#
#
import pandas as pd

goods = pd.DataFrame(pd.read_csv("jd_goods.csv", header=0, encoding="utf-8-sig"))
target_goods = goods["商品名称"]
print(target_goods)
with open("goods_title.txt", "w", encoding="utf-8") as fw:
    for v in target_goods.values:
        v = v.replace("\n", "").replace("\r", "").replace("\t", "")
        fw.write(v + "\n")
