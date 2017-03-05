# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 18:53:44 2017

@author: xk
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import random
import datetime
#采集一个网站所有的外链
 
pages = set()
random.seed(datetime.datetime.now())
 
allExtLinks = set()
allIntLinks = set()
 
def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html,'html.parser')
    internalLinks = getInternaLinks(bsObj,splitAddress(siteUrl)[0]) # 获得所有内链
    externalLinks = getExternalLinks(bsObj, splitAddress(siteUrl)[0]) # 获得所有外链
    #print(externalLinks)
    for link in externalLinks:
        if link not in allExtLinks: # 如果此外链没被记录在allExtLinks集合里
            allExtLinks.add(link) # 将此外链放入集合
            #print('外链：'+link)
    for link in internalLinks:
        print('内敛:'+link)
        if link not in allIntLinks:
            print("即将获取链接的URL是：" + link)
            allIntLinks.add(link)
            getAllExternalLinks(link)
    
 
 
# 获取页面所有内链的列表
def getInternaLinks(bsObj,includeUrl):
    internalLinks = []
    #找出所有以/开头的链接
    for link in bsObj.findAll('a',href = re.compile("^(/"+")")):
        if link.attrs['href'] is not None: # 如果此链接包含href属性
            if link.attrs['href'] not in internalLinks: # 如果此链接没有被放进internalLinks列表
                internalLinks.append(link.attrs['href'])
    return internalLinks
 
# 获取页面的所有外链列表
def getExternalLinks(bsObj,excludeUrl):
    externalLinks = []
    for link in bsObj.findAll('a',href = re.compile('^(http|www)((?!'+excludeUrl+').)*$')):# 找出所有以www或http开头且不包含当前url的链接
        if link.attrs['href'] is not None: # 如果此链接包含href属性
            if link.attrs['href'] not in externalLinks: # 如果此链接没有被放进externalLinks列表
                externalLinks.append(link.attrs['href'])
    return externalLinks
 
def splitAddress(address):
    addressParts = address.replace("http://","").split("/") # replace，表示在address中用空字符串替换http://  addressParts得到['www.oreilly.com','']
    return addressParts
 
def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html,'html.parser')
    externalLinks = getExternalLinks(bsObj,splitAddress(startingPage)[0]) # splitAddress(startingPage)[0]是www.oreilly.com
    if len(externalLinks) == 0: # 如果在www.oreilly.com中没找到外链
        internalLinks = getInternaLinks(bsObj,startingPage) # 从www.oreilly.com获取内链
        return getInternaLinks(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]
 
def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("随机外链是："+externalLink)
    followExternalOnly(externalLink)
 
# followExternalOnly("http://oreilly.com/")
#getInternaLinks()
getAllExternalLinks("http://www.cnki.net/")

