import os
import requests
from lxml import etree
import ConfigMsg
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

    def file_save_path(self, url):
        f_path = str(url).split("/doc", 1)[1]
        f_path = f_path.replace("/", "\\")
        fs_path = ConfigMsg.file_local + f_path
        dir_path = os.path.split(fs_path)[0]+"\\"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return fs_path

    def download_file(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        requests.packages.urllib3.disable_warnings()
        try:
            d_file = requests.get(url, headers=headers, verify=False)
            fs_path = self.file_save_path(url)
            if len(fs_path) > 250:
                fs_path = "\\\?\\" + fs_path
            with open(fs_path, "wb") as file:
                file.write(d_file.content)
        except Exception as e:
            raise Exception("error：下载出现错误")

    def Get_svnfile(self, url):
        filedownloadurl=[]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, verify=False)
        html = response.content.decode()
        element = etree.HTML(html)
        dir_lst = element.xpath('//dir')
        file_lst = element.xpath('//file')
        if len(dir_lst) == 0:
            # dir_lst= element.xpath('//file')
            for i in file_lst:
                # print(i.attrib["name"])
                href = url+str(i.attrib["name"])
                self.download_file(href)
                filedownloadurl.append(href)
            print(filedownloadurl)
            return filedownloadurl
        for i in dir_lst:
            print(i.attrib["name"])
            href = str(i.attrib["name"])
            # print(url+href)
            self.Get_svnfile(url+href+"/")
        for j in file_lst:
            href = str(j.attrib["name"])
            print(url + href)
            self.download_file(url+href)


    def Run_scrapsvnfile(self):
        print(".............start getsvnfile.............")
        self.Get_svnfile(self.url)
        print("..................finish ..................")


# url="https://192.168.10.201/svn/doc/QA测试/"
a = ScrapSvnFile("xuxb", "Justsy123", "https://192.168.10.201/svn/doc/QA测试/QA测试文档梳理/02 项目/J 建信金科/J 建亚BYOD/")
a.Run_scrapsvnfile()