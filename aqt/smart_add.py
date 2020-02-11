from PyQt5.QtWidgets import *
from aqt.forms import smart_add
from aqt.qt import *
from aqt.showwords import *
import aqt.forms
from aqt.utils import saveGeom, restoreGeom, showWarning, askUser, shortcut, \
    tooltip, openHelp, addCloseShortcut, downArrow, showInfo
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

        de_duplicate_words, duplicate_num, errormsg = self.mw.deckBrowser.de_duplicate_and_format(content)

        wordlist = self.mw.col.wordmatch(de_duplicate_words, level)
        #完成单词选择功能
        # showInfo("将导入以下单词，共{}个\n".format(len(words))  + str(words))
        new = Showwords(self.mw,wordlist)
        if new.exec_():
            words = new.getwordlist()
        else:
            # 这里填写 取消之后的操作
            words = new.getwordlist()

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
        report_add_res(len(wordlist), success_num, errormsg)
        self.form.textEdit.clear()

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
        # self.form.textEdit.clear()

    def _add_from_file(self):
        file_path = QFileDialog.getOpenFileName(None, '选择文件', './', "txt (*.txt)")[0]

        if not file_path:
            return
        if file_path.endswith('txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.form.textEdit.setText(content)
            # self.__add_words_by_content(content)
            # self.form.textEdit.clear()
        else:
            showWarning("必须是txt文件!")

