import threading
import ScrapSvnFile
import time

a = ScrapSvnFile.ScrapSvnFile("xuxb", "Justsy123", "https://192.168.10.201/svn/doc/QA测试/")

class MyThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            a.Get_svnfile(self.queue.get())


if __name__ == '__main__':
    start_time = time.time()
    a.Get_svn_dir_url(a.url)
    thread_lst = []
    for i in range(16):
        v = MyThread(a.file_queue)
        v.start()
        thread_lst.append(v)
    for i in thread_lst:
        i.join()
    print(len(a.totalfileurllst))
    finish_time = time.time()
    print("..................FINISH..................")
    print(finish_time - start_time)
