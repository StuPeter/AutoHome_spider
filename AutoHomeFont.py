#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/5/6
# @Author  : 圈圈烃
# @File    : AutoHomeFont
# @Description: 汽车之家字体反爬虫的解决方案
#
#
from fontTools import ttLib

# 选定作为标准字体的Unicode编码和对应文字
uni_tuple = (
            'uniED68', 'uniECB5', 'uniED06', 'uniEC53', 'uniECA5', 'uniEDE5', 'uniED32', 'uniED84', 'uniECD0', 'uniEC1D',
            'uniEC6F', 'uniEDAF', 'uniEE01', 'uniED4E', 'uniEC9A', 'uniECEC', 'uniEC39', 'uniED79', 'uniEDCB', 'uniED18',
            'uniED6A', 'uniECB6', 'uniEDF7', 'uniEC55', 'uniED95', 'uniECE2', 'uniED34', 'uniEC80', 'uniECD2', 'uniEC1F',
            'uniED5F', 'uniEDB1', 'uniECFE', 'uniEC4A', 'uniEC9C', 'uniEDDD', 'uniEC3A', 'uniED7B')
word_tuple = ('低', '很', '了', '呢', '十', '右', '大', '不', '高', '矮',
              '好', '和', '的', '地', '是', '长', '六', '二', '五', '短',
              '近', '七', '少', '四', '着', '多', '左', '一', '更', '得',
              '三', '坏', '八', '上', '下', '小', '远', '九')
new_uni_tuple = (
            '\\u4f4e', '\\u5f88', '\\u4e86', '\\u5462', '\\u5341', '\\u53f3', '\\u5927', '\\u4e0d', '\\u9ad8', '\\u77ee',
            '\\u597d', '\\u548c', '\\u7684', '\\u5730', '\\u662f', '\\u957f', '\\u516d', '\\u4e8c', '\\u4e94', '\\u77ed',
            '\\u8fd1', '\\u4e03', '\\u5c11', '\\u56db', '\\u7740', '\\u591a', '\\u5de6', '\\u4e00', '\\u66f4', '\\u5f97',
            '\\u4e09', '\\u574f', '\\u516b', '\\u4e0a', '\\u4e0b', '\\u5c0f', '\\u8fdc', '\\u4e5d',
)

def comparison(l1, l2):
    """比较新字体和标准字体坐标差"""
    if len(l1) != len(l2):
        return False
    else:
        for i in range(len(l1)):
            if abs(l1[i][0] - l2[i][0]) < 40 and abs(l1[i][1] - l2[i][1]) < 40:
                pass
            else:
                return False
        return True


def get_font_list(font, unilist):
    """获取字体坐标列表"""
    fontCoordinateList = []
    for uni in unilist:
        # 保存一个字符的(x,y)信息
        coordinateList = []
        # 获取对象的x,y信息，返回的是一个GlyphCoordinates对象，可以当作列表操作，每个元素是（x,y）元组
        wordGlyph = font['glyf'][uni].coordinates
        # 把GlyphCoordinates对象改成一个列表
        for wordLocation in wordGlyph:
            coordinateList.append(wordLocation)
        fontCoordinateList.append(coordinateList)
    return fontCoordinateList


def get_new_font_dict(standardFontPath, newFontPath):
    """获取新字体中的Unicode和汉字对应字典"""
    # 读取标准字体坐标
    standardFont = ttLib.TTFont(standardFontPath)
    standardCoordinateList = get_font_list(standardFont, uni_tuple)
    # 读取新字体坐标
    newFont = ttLib.TTFont(newFontPath)
    uni_list2 = newFont.getGlyphOrder()[1:]
    newCoordinateList = get_font_list(newFont, uni_list2)
    # 比较标准字体和新字体
    font_dict = {}
    for nc_idx, nc in enumerate(newCoordinateList):
        for sc_idx, sc in enumerate(standardCoordinateList):
            if comparison(sc, nc):
                font_dict[uni_list2[nc_idx]] = new_uni_tuple[sc_idx]
    print(font_dict)
    return font_dict


if __name__ == '__main__':
    standardFontPath = 'standardFont.ttf'
    newFontPath = '03.ttf'
    get_new_font_dict(standardFontPath, newFontPath)
