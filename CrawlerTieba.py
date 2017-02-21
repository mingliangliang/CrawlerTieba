# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:31:28 2017

@author: liang.ming
"""

import urllib2
import re

#---------------处理页面上的各种标签----------------
class HTML_Tool:
    #用非 贪婪模式 匹配 \t \n 空格 超链接 图片
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")
    #用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")
    #用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")
    
    #将一些HTML的符号实体转换为原始符号
    replaceTab = [("&lt;","<"),("&gt;",">"),("&amp;","&"),("&quot;","\""),("&nbsp;"," ")]
    
    def Replace_Char(self,x):
        x = self.BgnCharToNoneRex.sub("",x)
        x = self.BgnPartRex.sub("\n   ",x)
        x = self.CharToNewLineRex.sub("\n",x)
        x = self.CharToNextTabRex.sub("\t",x)
        x = self.EndCharToNoneRex.sub("",x)
        
        for t in self.replaceTab:
            x = x.replace(t[0],t[1])
        return x
        
        
class Baidu_Crawler:
    def __init__(self,url):
        self.myUrl = url + '?see_lz=1'
        self.datas = []
        self.myTool = HTML_Tool()
        print u'已经启动贴吧爬虫'
        
    #初始化加载页面并将其转码存储
    def baidu_tieba(self):
        # 读取页面的原始信息并将其转码
        myPage = urllib2.urlopen(self.myUrl).read().decode("utf-8")
        # 计算楼主发布内容总页数
        endPage = self.page_counter(myPage)
        # 获取标题
        title = self.find_title(myPage)
        print u'文章标题：' + title
        #获取最终数据
        self.save_data(self.myUrl,title,endPage)
        
    #计算总页数
    def page_counter(self,myPage):
        myMatch = re.search(r'class="red">(\d+?)</span>', myPage, re.S)
        if myMatch:
            endPage = int(myMatch.group(1))
            print u'爬虫报告：发现楼主共有%d页的原创内容' % endPage
        else:
            endPage = 0
            print u'爬虫报告：无法计算楼主发布内容有多少页'
        return endPage
        
    #提取标题
    def find_title(self,myPage):
        myMatch = re.search(r'<h3.*?>(.*?)</h3>', myPage, re.S)
        title = u'暂无标题'
        if myMatch:
            title = myMatch.group(1)
        else:
            print u'爬虫报告：无法加载文章标题！'
        title = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')
        return title
        
        
    # 用来存储楼主发布的内容
    def save_data(self,url,title,endPage):
        # 加载页面数据到数组中
        self.get_data(url,endPage)
        # 打开本地文件
        f = open(title+'.txt','w+')
        f.writelines(self.datas)
        f.close()
        print u'爬虫报告：文件已下载到本地'
        print u'请按任意键退出...'
        raw_input();

    # 获取页面源码并将其存储到数组中
    def get_data(self, url, endPage):
        url = url + '&pn='
        for i in range(1,endPage+1):
            print u'爬虫报告：爬虫%d号正在工作中...' % i
            myPage = urllib2.urlopen(url+str(i)).read()
            # 将myPage中的HTML代码处理并存储到datas里面
            self.deal_data(myPage.decode('utf-8'))
            
    # 将内容从源码中抠出
    def deal_data(self,myPage):
        myItems = re.findall('id="post_content.*?>(.*?)</div>',myPage,re.S)
        for item in myItems:
            data = self.myTool.Replace_Char(item.replace("\n","").encode('utf-8'))
            self.datas.append(data+'\n')
    
    
#-------- 程序入口处 ------------------
print u"""#---------------------------------------
#   程序：百度贴吧爬虫
#   版本：0.1
#   作者：liang.ming
#   日期：2017-02-15
#   语言：Python 2.7
#   操作：输入网址后自动只看楼主并保存到本地文件
#   功能：将楼主发布的内容打包txt存储到本地。
#---------------------------------------
"""
    
# 以某小说贴吧为例子
# bdurl = 'http://tieba.baidu.com/p/4318303215?see_lz=1&pn=1'    
    
print u'请输入贴吧的地址最后的数字串：'
bdurl = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/4318303215'))     
    
    
#调用
myCrawler = Baidu_Crawler(bdurl)
myCrawler.baidu_tieba()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    