import os
import requests
from lxml import etree


# E:\CodeProject\ScrapSvnFile
root_path = os.path.split(os.path.realpath(__file__))[0]


class ScrapSvnFile():
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def deal_url(self, url):
        login_msg = str(self.username) + ":" + str(self.password) + "@"
        font_url = str(url).split("//", 1)[0]
        back_url = str(url).split("//", 1)[1]
        url = font_url + "//" + login_msg + back_url
        print(url)
        return url

    def Get_svnfile(self, url):
        url = self.deal_url(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        response = requests.get(url, headers=headers)
        html = response.content.decode()
        element = etree.HTML(html)
        statuslst = element.xpath('//svn/dir')
        for i in statuslst:
            print(i)
            href = i.xpath('/a/@href')
            print(href)

    def Run_scrapsvnfile(self):
        print("start getsvnfile........")
        self.Get_svnfile(self.url)
        print("finish ..................")




# url="https://192.168.10.201/svn/doc/QA测试/"
a= ScrapSvnFile("xuxb","Justsy123","https://192.168.10.201/svn/doc/QA测试/")