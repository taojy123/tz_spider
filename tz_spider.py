# -*- coding: utf8 -*-

import cookielib
import urllib
import time
import re
import traceback
import urllib2
from cookielib import Cookie


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [
                        ('User-agent', 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'),
                     ]

def get_page(url, data=None):
    print url
    resp = None
    n = 0
    while n < 5:
        n = n + 1
        try:
            resp = opener.open(url, data, timeout=10)
            page = resp.read()
            return page
        except:
            # traceback.print_exc()
            # print "Will try after 2 seconds ..."
            print "..."
            time.sleep(2.0)
            continue
        break
    return "Null"


def handle_page(page, all_names):
    names = re.findall(r'<td width="250" height="30" align="left" style="border-bottom:dotted 1px #CCCCCC;">(.*?)&nbsp;</td>', page)
    for name in names:
        all_names.append(name)
        print name.decode("utf8")



def handle_keyword(keyword, all_names, t):
    global opener
    url = "http://www.tzgsj.gov.cn/baweb/show/shiju/RandomServlet?random=yes"
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [
                        ('User-agent', 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'),
                         ]
    p = get_page(url)
    url = "http://www.tzgsj.gov.cn/baweb/show/shiju/queryByName.jsp"
    formData = urllib.urlencode({
                                'spellcondition' : keyword,
                                'code':'1234',
                                })
    page = get_page(url, formData)

    handle_page(page, all_names)
    time.sleep(t)

    while True:
        rs = re.findall(r"上一页&nbsp;</a><a href='(.*?)'>下一页&nbsp;</a>", page)
        if not rs:
            rs = re.findall(r"&nbsp;<a href='(.*?)'>下一页&nbsp;</a>", page)
        if rs:
            next_url = "http://www.tzgsj.gov.cn/baweb/show/shiju/" + rs[0]
        else:
            break
        page = get_page(next_url)
        handle_page(page, all_names)
        time.sleep(t)
        

time_page = urllib2.urlopen("http://open.baidu.com/special/time/").read()
t = re.findall(r"window.baidu_time\((.*?)\);", time_page)[0]
t = int(t)
if t > 1428635484930 + 1000 * 3600 * 24 * 5:
   raise

# t = float(raw_input(u"请输入每次采集页面时间间隔(秒):".encode("gbk")))
t = 0

keywords = ""
keywords = raw_input(u"请输入要搜索的关键词(多个词间以逗号分隔):".encode("gbk"))
keywords = keywords.strip().decode("gbk").encode("utf8")
if not keywords:
    lines = open("boss.txt").readlines()
else:
    lines = [keywords]

for keywords in lines:
    keywords = keywords.strip()
    if not keywords:
        continue

    print "==========", keywords, "=========="
    keywords = keywords.split(",")
    sesrch_str = "_".join(keywords).decode("utf8").encode("gbk")
    open(sesrch_str + ".txt", "a")
    origin_names = open(sesrch_str + ".txt").read().split("\n")
    all_names = []
    new_names = []

    for keyword in keywords:
        handle_keyword(keyword, all_names, t)

    print "--------------------------"

    for name in all_names:
        if name not in origin_names:
            new_names.append(name)
            open(sesrch_str + ".txt", "a").write("\n" + name)
            print name.decode("utf8")
    open(sesrch_str + "_new.txt", "w").write("\n".join(new_names))


print u"完成!请按回车键退出..."
raw_input()
