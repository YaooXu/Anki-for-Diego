import requests
import json
from PyQt5.QtWidgets import QMessageBox
import threading


def report_add_res(tot_num, success_num):
    fail_num = tot_num - success_num
    alert = QMessageBox()
    content = "共%d个单词，添加成功%d个，失败%d个" % (tot_num, success_num, fail_num)
    alert.setText(content)
    alert.exec_()


def get_word(word, timeout=5):
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
    url = u"http://mall.baicizhan.com/ws/search?w={word}".format(word=word)
    print(url)
    response = requests.get(url)
    result = response.json()
    if len(result) == 1:
        result['errorCode'] = 1
    else:
        result['sound'] = "http://baicizhan.qiniucdn.com/word_audios/" + word + ".mp3"

    print(result)
    if result['errorCode'] == 1:
        return None
    else:
        return result


class MyThread(threading.Thread):
    def __init__(self, word, timeout=5):
        super(MyThread, self).__init__()  # 重构run函数必须要写
        self.word = word
        self.timeout = timeout

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
        if result['errorCode'] == 1:
            return None
        else:
            return result


if __name__ == '__main__':
    #word_info = get_word('test')
    t1=MyThread('test')
    t2=MyThread('file')
    t1.start()
    t2.start()
    #将t1,t2加入主线程
    t1.join()
    t2.join()