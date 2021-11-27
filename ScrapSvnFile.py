import hashlib
import os
import requests
from lxml import etree
import ConfigMsg
import time
import datetime
import SaveMsgInSql
import urllib3


# E:\CodeProject\ScrapSvnFile
root_path = os.path.split(os.path.realpath(__file__))[0]


class ScrapSvnFile():
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = self.deal_url(url)
        self.totalfileurllst = []
        self.filemd5lst = []

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

    def save_msg_in_lst(self, name, parent_path, url):
        ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        self.filemd5lst.append(file_md5)
        msg_lst = tuple([name, parent_path, file_md5, url, ctime])
        return msg_lst

    def Get_svnfile(self, url):
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
                name = i.attrib["name"]
                href = url + name
                parent_path = str(url).split("/doc", 1)[1]
                self.totalfileurllst.append(self.save_msg_in_lst(name, parent_path, href))
            # print(filedownloadurl)
            return 0
        for i in dir_lst:
            # print(i.attrib["name"])
            href = str(i.attrib["name"])
            # print(url+href)
            self.Get_svnfile(url+href+"/")
        for j in file_lst:
            name = str(j.attrib["name"])
            href = url + name
            parent_path = str(url).split("/doc", 1)[1]
            # print(url + href)
            self.totalfileurllst.append(self.save_msg_in_lst(name, parent_path, href))
            # self.download_file(url+href)


    def Run_scrapsvnfile(self):
        start_time = time.time()
        print(".............start getsvnfile.............")
        self.Get_svnfile(self.url)
        print("..................finish ..................")
        print("..................INSERT INTO SQL..................")
        add_svn_data = []
        delete_sql_data = []
        svn_data = self.totalfileurllst
        sql_msg = SaveMsgInSql.SaveMsgInSql()
        #获取原有数据
        original_data = sql_msg.conn_get_msg()
        print(original_data)
        for i in svn_data:
            if i[2] not in original_data:
                add_svn_data.append(i)
        for j in original_data:
            if j not in self.filemd5lst:
                delete_sql_data.append(j)
        print("add++++++",add_svn_data)
        print("del------",delete_sql_data)
        #增量插入数据库
        sql_msg.conn_save_msg(tuple(add_svn_data))
        #删除多余数据
        sql_msg.conn_delete_msg(tuple(delete_sql_data))
        finish_time = time.time()
        print("..................INSERT FINISH..................")
        print(finish_time - start_time)


# url="https://192.168.10.201/svn/doc/QA测试/"
a = ScrapSvnFile("xuxb", "Justsy123", "https://192.168.10.201/svn/doc/QA测试/")
a.Run_scrapsvnfile()
