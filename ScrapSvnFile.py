import os
import requests
from lxml import etree
import urllib3


# E:\CodeProject\ScrapSvnFile
root_path = os.path.split(os.path.realpath(__file__))[0]


class ScrapSvnFile():
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = self.deal_url(url)

    def deal_url(self, url):
        login_msg = str(self.username) + ":" + str(self.password) + "@"
        font_url = str(url).split("//", 1)[0]
        back_url = str(url).split("//", 1)[1]
        url = font_url + "//" + login_msg + back_url
        print(url)
        return url

    def Get_svnfile(self, url):
        a=[]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, verify=False)
        html = response.content.decode()
        element = etree.HTML(html)
        statuslst = element.xpath('//dir')
        if len(statuslst)== 0:
            statuslst= element.xpath('//file')
            for i in statuslst:
                # print(i.attrib["name"])
                a.append(str(i.attrib["name"]))
            print(a)
            return a
        for i in statuslst:
            print(i.attrib["name"])
            href = str(i.attrib["href"])
            print(url+href)
            self.Get_svnfile(url+href)


    def Run_scrapsvnfile(self):
        print(".............start getsvnfile.............")
        self.Get_svnfile(self.url)
        print("..................finish ..................")


# url="https://192.168.10.201/svn/doc/QA测试/"
a = ScrapSvnFile("xuxb","Justsy123","https://192.168.10.201/svn/doc/QA测试/")
a.Run_scrapsvnfile()