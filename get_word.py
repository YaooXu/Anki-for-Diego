from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import json
import threading
import time
from aqt.utils import showInfo

SearchLock = threading.Lock()
Emit = 0


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


from bs4 import BeautifulSoup


def get_from_Baicizhan(word, timeout=5):
    r"""
    从百词斩获得单词
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
        "errormsg" 返回码。0代表正常，-2是网络超时， -1是其他错误
    }
    """
    try:
        url = u"http://mall.baicizhan.com/ws/search?w={word}".format(word=word)
        response = requests.get(url)
        result = response.json()
        if len(result) == 1:
            result['errormsg'] = -1
            return result
        result['sound'] = "http://baicizhan.qiniucdn.com/word_audios/" + word + ".mp3"
        result['errormsg'] = 0
    except  requests.exceptions.RequestException:
        result = {}
        result['errormsg'] = -2
    except Exception:
        result = {}
        result['errormsg'] = -1
    return result


def get_from_Youdao(words, timeout=5):
    """
    {'word' : 'apple'
    'us-phonetic': 'ˈæpl',
    'phonetic': 'ˈæpl',
    'uk-phonetic': 'ˈæpl',
    'explains': 'n. 苹果，苹果树，苹果似的东西；[美俚]炸弹，手榴弹，（棒球的）球；[美俚]人，家伙。',
    'sound': 'http://dict.youdao.com/dictvoice?type=0&audio=apple.mp3',
    'errormsg': 0}
    """
    result = {}
    try:
        URL = 'http://fanyi.youdao.com/openapi.do?keyfrom=youdaoci&key=694691143&type=data&doctype=json&version=1.1'
        result = requests.get(URL + '&q=' + words, timeout=timeout)
        result = result.json()
        result = result['basic']
        result['explains'] = result['explains'][0]
        result['word'] = words
        result['sound'] = "http://dict.youdao.com/dictvoice?type=0&audio=" + words + ".mp3"  # 美音 type=0 英音type=1
        result['errormsg'] = 0
    except  requests.exceptions.RequestException:
        result = {}
        result['errormsg'] = -2
    except Exception:
        result = {}
        result['errormsg'] = -1
    return result


def _get_element(soup, tag, id=None, class_=None, subtag=None):
    # element = soup.find(tag, id=id, class_=class_)  # bs4
    """
    爬虫辅助函数，获取soup中的相关信息
    """
    element = None
    if id:
        element = soup.find(tag, {"id": id})
    if class_:
        element = soup.find(tag, {"class": class_})
    if subtag and element:
        element = getattr(element, subtag, '')
    return element


def get_from_Bing(word, timeout=5):
    """
    爬取bing词典
    {
        'word' : 'apple'
        'phonitic_us': '美 [ˈæp(ə)l] ',
        'phonitic_uk': "英 ['æpl] ",
        'participle': '复数：apples  ',
        'def': 'n.苹果公司；【植】苹果；【植】苹果树网络苹果电脑；美国苹果；美国苹果公司',
        'errormsg': 0
    }
    phonitic_us：美式发音
    phonitic_uk：英式发音
    participle：词语时态
    def：释义
    """
    result = {}
    try:
        req = requests.get(url=
                           "http://cn.bing.com/dict/search?q={}&mkt=zh-cn".format(word), timeout=timeout)
        req.encoding = req.apparent_encoding
        data = req.text
        soup = BeautifulSoup(data, "html.parser")
        result['word'] = word
        element = _get_element(soup, 'div', class_='hd_prUS').get_text()
        if element:
            result['phonitic_us'] = str(element).replace('\xa0', ' ')
        element = _get_element(soup, 'div', class_='hd_pr').get_text()
        if element:
            result['phonitic_uk'] = str(element).replace('\xa0', ' ')
        element = _get_element(soup, 'div', class_='hd_if').get_text()
        if element:
            result['participle'] = str(element).replace('\xa0', ' ')
        element = _get_element(soup, 'div', class_='qdef', subtag='ul')
        if element:
            result['def'] = u''.join([str(content.get_text())
                                      for content in element.contents])
        result['errormsg'] = 0
    except  requests.exceptions.RequestException:
        result = {}
        result['errormsg'] = -2
    except Exception:
        result = {}
        result['errormsg'] = -1
    return result


def get_from_Iciba(word, timeout=5):
    '''
    {
        'word' : 'apple'
        'ph_am': 'ˈæpəl',
        'ph_en': 'ˈæpl',
        'ph_am_mp3': 'http://res.iciba.com/resource/amp3/1/0/1f/38/1f3870be274f6c49b3e31a0c6728957f.mp3',
        'ph_en_mp3': 'http://res.iciba.com/resource/amp3/oxford/0/44/29/44297283b5e4b5b0a991213897f0b14a.mp3',
        'parts': 'n. 苹果; 苹果树; 苹果公司',
        'sentence': 'What will be the effect of the alliance between IBM and Apple?\n若IBM公司和苹果公司联手将会有什么效果呢？\n',
        'errormsg': 0
        }
    '''
    result = {}
    try:
        URL = 'http://www.iciba.com/index.php?a=getWordMean&c=search&word='
        query = requests.get(URL + word, timeout=timeout)
        query = query.json()
        result['word'] = word
        result['ph_am'] = query["baesInfo"]['symbols'][0]['ph_am']  # 美式音标
        result['ph_en'] = query["baesInfo"]['symbols'][0]['ph_en']  # 英式音标
        result['ph_am_mp3'] = query["baesInfo"]['symbols'][0]['ph_am_mp3']  # 美式发音
        result['ph_en_mp3'] = query["baesInfo"]['symbols'][0]['ph_en_mp3']  # 英式发音
        parts = query["baesInfo"]['symbols'][0]['parts']
        result['parts'] = u'<br>'.join([part['part'] + ' ' + '; '.join(part['means']) for part in parts])  # 释义
        sentences = ''
        segs = query["sentence"]
        if segs:
            sentences = segs[0]['Network_en'] + '\n' + segs[0]['Network_cn'] + '\n'
        result['sentence'] = sentences  # 双语例句
        result['errormsg'] = 0
    except  requests.exceptions.RequestException:
        result = {}
        result['errormsg'] = -2
    except Exception:
        result = {}
        result['errormsg'] = -1
    return result


source_func_map = {
    'Baicizhan': get_from_Baicizhan,
    'Youdao': get_from_Youdao,
    'Bing': get_from_Bing,
    'Iciba': get_from_Iciba
}


class WordThread(QThread):
    query_finish = pyqtSignal()

    def __init__(self, word, source_list, timeout=5):
        super().__init__()
        self.word = word
        self.source_list = source_list
        self.timeout = timeout
        self.word_info = None

    def run(self):
        all_res = {}
        for source_name in self.source_list:
            func = source_func_map[source_name]
            res = func(self.word, self.timeout)
            all_res[source_name] = res
        self.word_info = all_res
        SearchLock.acquire()
        try:
            global Emit
            Emit += 1
        finally:
            SearchLock.release()
        # self.query_finish.emit()

    def get_info(self):
        return self.word_info

    def __del__(self):
        self.wait()


class WordsAdder(QWidget):
    def __init__(self, browser, word_list, source_list, timeout=5):
        """

        :param word_list: 单词列表
        :param source_list: 来源列表
        :param timeout: 最长时间
        """
        super().__init__()
        self.words_num = len(word_list)
        self.cur_num = 0
        self.browser = browser

        # 设置进度条
        self.progress = QProgressDialog(self)
        self.progress.setWindowTitle("请稍等")
        self.progress.setLabelText("正在查询单词...")
        self.progress.setCancelButtonText("取消")
        self.progress.setMinimumDuration(5)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setRange(0, 100)
        self.progress.setValue(1)
        self.progress.show()

        self.threads = []
        global Emit
        Emit = 0
        for word in word_list:
            thread = WordThread(word, source_list, timeout)
            self.threads.append(thread)
            # thread.query_finish.connect(self.change_progress_dialog)
            thread.start()

        while True:
            if Emit != self.words_num:
                self.progress.setValue(Emit * 100 / self.words_num)
                continue
            else:
                break
        self.progress.setLabelText("查询完成, 正在添加")
        self.progress.close()
        # 所有单词的最终信息
        self.word_infos = []

    def change_progress_dialog(self):
        # TODO:因为查询单词的速度太快了，这个好像有点跟不上...
        # 所以有时候这块显示有点问题
        # 可以改为直接在查询单词的线程里面setValue而不是通过信号
        self.cur_num += 1
        print(self.cur_num)
        self.progress.setValue(self.cur_num * 100 / self.words_num)
        if self.cur_num == self.words_num:
            self.progress.setLabelText("查询完成, 正在添加")
            self.progress.close()

    def get_res(self):
        for thread in self.threads:
            thread.wait()

        for thread in self.threads:
            word_info = thread.get_info()
            if word_info:
                self.word_infos.append(word_info)

        return self.word_infos
        # self.browser.add_words(self.word_infos)
        # report_add_res(self.words_num, len(self.word_infos))


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
