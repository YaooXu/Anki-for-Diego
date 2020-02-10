from PyQt5.QtWidgets import *
from aqt.forms import smart_add
from aqt.qt import *
import aqt.forms
from aqt.utils import saveGeom, restoreGeom, showWarning, askUser, shortcut, \
    tooltip, openHelp, addCloseShortcut, downArrow
from anki.get_word import report_add_res, WordsAdder
import json

class SmartAdd( QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, None, Qt.Window)
        mw.setupDialogGC(self)
        self.mw = mw
        self.form = smart_add.Ui_SmartAdd()
        self.form.setupUi(self)
        # 设置connect
        self.form.file_choose_bt.clicked.connect(self._add_from_file)
        self.form.smart_add_bt.clicked.connect(self._add_from_text)
        self.show()

    # 添加单词
    ##########################################################################
    def __add_words_by_content(self, content):
        # 根据content得到所有单词的信息
        # 并添加单词
        """
        :param content:
        :return: words (list of string)
                 word_infos (list of dict)
        """
        level = ""
        if self.form.primary.isChecked():
            level = "xx"
        elif self.form.middle.isChecked():
            level = "zk"
        elif self.form.high.isChecked():
            level = "gk"
        elif self.form.cet4.isChecked():
            level = "cet4"
        elif self.form.cet6.isChecked():
            level = "cet6"

        if level == "":
            showWarning("请选择等级")
            return

        source = self.mw.col.models.getCurrentSource()
        if not source:
            showWarning("未指定导入模板!")
            return

        # 这个模板所需要的所有来源 ex: ['Baicizhan', 'Youdao']
        source_list = []
        for key, val in source.items():
            source_name = val.split(':')[0]
            if source_name not in source_list:
                source_list.append(source_name)

        origin_words = content.strip().split('\n')
        index = 0
        # 保证了添加单词的顺序，且剔除空格
        while True:
            cnt = index
            if index == len(origin_words):
                break
            if " " in origin_words[index]:
                for tmp in origin_words[index].split(' '):
                    if tmp != "":
                        if  not tmp[-1].isalpha():#去掉常见标点
                            tmp = tmp[0:-1]
                        origin_words.insert(cnt + 1, tmp)
                        cnt = cnt + 1
                del origin_words[index]
                index = cnt
            else:
                index = index + 1

        # 文本框去重
        duplicate_words = {}
        errormsg = {}

        for i in origin_words:
            if i in duplicate_words.keys():
                duplicate_words[i] += 1
            else:
                duplicate_words[i] = 1
        words_temp = []
        for i in duplicate_words.keys():
            words_temp.append(i)

        # 牌库去重
        de_duplicate_words = []
        note = self.mw.col.newNote()
        for i in words_temp:
            if note.newDupeOrEmpty(i) != 2:
                de_duplicate_words.append(i)
            else:
                errormsg[i] = -3

        words = self.mw.col.wordmatch(de_duplicate_words, level)
        # 查询单词模板只负责查询，添加由自己完成，避免过度耦合
        adder = WordsAdder(self, words, source_list)
        word_infos = adder.get_res()

        check_word_infos = word_infos.copy()
        count = [-1, -1]
        flag = 0
        for word_info in check_word_infos:
            count[0] += 1
            count[1] += 1
            for key in word_info.keys():
                if flag == 1:
                    flag = 0
                    break
                for key2 in word_info[key]:
                    if key2 == 'errormsg' and word_info[key][key2] != 0:
                        errormsg[words[count[1]]] = word_info[key][key2]
                        del word_infos[count[0]]
                        count[0] -= 1
                        flag = 1
                        break

        success_num = self.mw.deckBrowser.add_words(word_infos)
        report_add_res(len(de_duplicate_words), success_num, errormsg)

    def _add_from_text(self):
        """
        :param content: textarea中的内容
        :return:
        """
        content = self.form.textEdit.toPlainText()
        if not content:
            showWarning("当前文本框为空")
            return
        self.__add_words_by_content(content)
        self.form.textEdit.clear()

    def _add_from_file(self):
        file_path = QFileDialog.getOpenFileName(None, '选择文件', './', "txt (*.txt)")[0]

        if not file_path:
            return

        if file_path.endswith('txt'):
            with open(file_path, 'r') as f:
                content = f.read()
            self.form.textEdit.setText(content)
            self.__add_words_by_content(content)
            self.form.textEdit.clear()
        else:
            showWarning("必须是txt文件!")
