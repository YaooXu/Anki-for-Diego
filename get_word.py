from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import json
import threading
import time



class MyBar(QWidget):

    def __init__(self, threads, browser):
        super(MyBar, self).__init__()
        super().__init__()
        self.threads = threads
        self.len = len(threads)
        self.now = 0
        self.browser = browser

    def setupUi(self):
        print("####################\n")
        self.setFixedSize(500, 90)
        self.main_widget = QtWidgets.QWidget(self)
        self.progressBar = QtWidgets.QProgressBar(self.main_widget)
        self.progressBar.setGeometry(QtCore.QRect(20, 20, 450, 50))
        # 创建并启用子线程
        self.thread_1 = Worker(self.threads)
        self.thread_1.progressBarValue.connect(self.copy_file)
        self.thread_1.start()

    def copy_file(self, i):
        self.now = self.now + 1
        self.progressBar.setValue(self.now * 100 / self.len)
        if self.now == self.len:
            self.browser.my_add(self.get_word_infos())
            res_to_show = ""
            for info in self.get_word_infos():
                res_to_show += str(info) + '\n'
            messageBox = QMessageBox()
            messageBox.setText(res_to_show)
            messageBox.exec_()
            report_add_res(self.len, len(self.get_word_infos()))

    def get_word_infos(self):
        return self.thread_1.get_word_infos()


class Worker(QThread):
    progressBarValue = pyqtSignal(int)  # 更新进度条

    def __init__(self, threads):
        super(Worker, self).__init__()
        self.threads = threads
        self.word_infos = []

    def get_word_infos(self):
        return self.word_infos

    def run(self):
        for i in range(len(self.threads)):
            self.threads[i].join()
            # time.sleep(1)
            info = self.threads[i].get_result()
            self.word_infos.append(info)
            self.progressBarValue.emit(1)  # 发送进度条的值信号


def report_add_res(tot_num, success_num):
    fail_num = tot_num - success_num
    alert = QMessageBox()
    content = "共%d个单词，添加成功%d个，失败%d个" % (tot_num, success_num, fail_num)
    alert.setText(content)
    alert.exec_()


class MyThread(threading.Thread):
    def __init__(self, word, timeout=5):
        super(MyThread, self).__init__()  # 重构run函数必须要写
        self.word = word
        self.timeout = timeout
        self.result = None

    def get_result(self):
        return self.result

    def run(self):
        r"""

        :param word: 需要查询的单词
        :param timeout: 时间限制
        :return: 如果查询成功，返回该单词的信息的字典，否则返回None
        {
            "word": 单词 str
            "img": 图片的网页链接 str
            "st":例句 str
            "sttr":例句翻译 str
            "mean_cn": 中文释义 str
            "accent": 音标 str
            "sound": 发音的链接 str
        }
        """
        url = u"http://mall.baicizhan.com/ws/search?w={word}".format(word=self.word)
        print(url)
        response = requests.get(url)
        result = response.json()
        if len(result) == 1:
            result['errorCode'] = 1
        else:
            result['sound'] = "http://baicizhan.qiniucdn.com/word_audios/" + self.word + ".mp3"

        print(result)
        self.result = result
        if result['errorCode'] == 1:
            return None
        else:
            return result


if __name__ == '__main__':
    # word_info = get_word('test')
    t1 = MyThread('test')
    t2 = MyThread('file')
    t1.start()
    t2.start()
    # 将t1,t2加入主线程
    t1.join()
    t2.join()
    print(t1.get_result())
    print(t2.get_result())
    print(t1.get_result())
