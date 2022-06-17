

# **注：汽车之家接口变化，项目已经失效**

# ~~汽车之家爬虫(AutoHome_spider)~~



[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org)

> 把人类从重复的劳动中解放出来，去创造新的事物。
## 

## 简介(Introduction)

~~汽车之家可以说是非常大的一个汽车论坛了，本项目是为了研究某款车型的口碑开发的，能够定向的获取某款车型的帖子以及评论。解决了该网站的字体反爬虫。~~

**汽车之家接口变化，项目已经失效**

## 快速开始(Quick start)

#### 环境要求(Requirements):

* Python 3.x (2.x is not supported)
* requests
* bs4
* fontTools
* pyecharts (绘图，只用爬虫无需此库)
* snownlp (自然语言处理，只用爬虫无需此库)

#### 操作步骤(Steps):

1. Git本项目到您的电脑上，或是直接Fork到您自己的仓库

        git clone https://github.com/StuPeter/AutoHome_spider.git

2. 目录结构如下：

        .
        ├── TTF
        │   ├── 03.ttf
        │   ├── standardFont.ttf
        │   └── temp.ttf
        ├── AnalysisData.py
        ├── AutoHomeFont.py
        ├── AutoHomeSpiderClass.py
        ├── main.py
        ├── targetCarUrl.txt
        ├── requirements.txt
        └── Readme.md
    
    + `TTF`文件夹为字体包；`03.ttf`为测试字体；`standardFont.ttf`为标准字体用于对比；`temp.ttf`为临时字体是每次下载会自动替换；
    + `AnalysisData.py`为我自己的分析程序，对您基本没用；
    + `AutoHomeFont.py`为字体替换程序，用于解决汽车之家的字体反爬；
    + `AutoHomeSpiderClass.py`为解析和下载的类，供main.py调用；
    + `main.py`为主程序，用于爬取帖子；
    + `targetCarUrl.txt`存储车型论坛链接和ID，可自动更新；
    
3. 在开始之前，需要先打开`main.py`，拉到最底部可以看到如下程序：

        if __name__ == '__main__':
            # 更新targetCarUrl.txt
            updateCarUrl()
            # 爬虫主程序
            #main(pageIndex=1, BBSId=352)
    
   建议您先注释 **main()** ，运行 **updateCarUrl()** 。这会帮您更新`targetCarUrl.txt`，在该文件中，您可以获取您想要车型的BBSId。
   其中 **updateCarUrl()** 可以传入参数，例如 **updateCarUrl("奔驰")**，将只会获取所有奔驰车型的BBSId。

4. 同样在`main.py`中：

   注释 **updateCarUrl()**，填入 **main()** 函数的参数：pageIndex和BBSId，其中pageIndex为该车型论谈的页码，BBSId可去`targetCarUrl.txt`中查找。

5. 如上设置设置完毕后，直接运行main.py即可。ps:由于是单线程下载，可能需要较长时间，如果是固定IP请注意爬取的时间间隔，默认2秒。

6. 最后爬取完毕后，会生成`你选定的BBSId_post.csv`里面的数据格式如下：

         ['用户名', '精华帖数量', '发帖量', '回帖量', '注册日期', '地理位置', '回复日期', '回复内容']

## 许可(License)
[MIT license](https://github.com/StuPeter/Sougou_dict_spider/blob/master/LICENSE "MIT license")
    

