# Copyright: Ankitects Pty Ltd and contributors
# -*- coding: utf-8 -*-
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
import time
from aqt.qt import *
from aqt.utils import askUser, getOnlyText, openLink, showWarning, shortcut, \
    openHelp
from anki.utils import ids2str, fmtTimeSpan
from anki.errors import DeckRenameError
import aqt
from anki.sound import clearAudioQueue
from anki.hooks import runHook
from copy import deepcopy
from anki.lang import _, ngettext
import requests
from anki.get_word import report_add_res, WordsAdder
import json

# 牌组浏览
class DeckBrowser:

    def __init__(self, mw):
        self.mw = mw
        self.web = mw.web
        self.bottom = aqt.toolbar.BottomBar(mw, mw.bottomWeb)
        self.scrollPos = QPoint(0, 0)

    def show(self):
        clearAudioQueue()
        # 重置点击处理
        self.web.resetHandlers()
        self.web.onBridgeCmd = self._linkHandler
        self._renderPage()

    def refresh(self):
        self._renderPage()

    # 处理事件
    ##########################################################################

    def _linkHandler(self, url):
        if ":" in url:
            (cmd, arg) = url.split(":")
        else:
            cmd = url
        if cmd == "open":
            self._selDeck(arg)
        elif cmd == "opts":
            self._showOptions(arg)
        elif cmd == "shared":
            self._onShared()
        elif cmd == "import":
            self.mw.onImport()
        elif cmd == "lots":
            openHelp("using-decks-appropriately")
        elif cmd == "hidelots":
            self.mw.pm.profile['hideDeckLotsMsg'] = True
            self.refresh()
        elif cmd == "create":
            deck = getOnlyText(_("Name for deck:"))
            if deck:
                self.mw.col.decks.id(deck)
                self.refresh()
        elif cmd == "drag":
            draggedDeckDid, ontoDeckDid = arg.split(',')
            self._dragDeckOnto(draggedDeckDid, ontoDeckDid)
        elif cmd == "collapse":
            self._collapse(arg)
        elif cmd == "add_from_text":
            print(cmd, arg)
            self._add_from_text(arg)
        elif cmd == "add_from_file":
            print(cmd)
            self._add_from_file()
        elif cmd == "import_model":
            self._import_model()
        elif cmd == 'change_model':
            self._change_model(arg)
        return False

    def _selDeck(self, did):
        self.mw.col.decks.select(did)
        self.mw.onOverview()

    # HTML generation
    ##########################################################################
    # 主体部分的html
    _body = """
<center>
<table cellspacing=0 cellpading=3>
%(tree)s
</table>

<br>
%(stats)s
%(countwarn)s
</center>
"""
    # 添加单词部分的html
    _add_word_body = """
<center>
<br>
<br>
<hr style=" width: 30em;border-color: black;">
        <div class="buttonbox">
            <div><textarea id="words-area"></textarea></div>
            <div class="buttonlist">
                <label>请选择模板</label>
                <br>
                <br>
                <select id='choose_model'>
                    %(models)s
                </select>
                <br>
                <br>
                <button type="button" id="import_model">导入新的模板</button>
                <br>
                <br>
                <hr style=" width: 12em;border-color: black;">
                <br>
                <button type="button" id="add_from_text_bt">添加文本框中单词</button>
                <br>
                <br>
                <button type="button" id="add_from_file_bt">从文件导入单词</button>
                <br>
                <br>
                
            </div>

        </div>
        <hr style=" width: 30em;border-color: black;">
</center>
"""

    def _renderPage(self, reuse=False):
        if not reuse:
            self._dueTree = self.mw.col.sched.deckDueTree()
            self.__renderPage(None)
            return
        self.web.evalWithCallback("window.pageYOffset", self.__renderPage)

    def __renderPage(self, offset):
        # 加载所有牌组信息的html
        tree = self._renderDeckTree(self._dueTree)
        stats = self._renderStats()
        models = self._renderModels()
        # 点击html中的某个链接会返回一个类似于pycmd('open:1')的东西
        # 其中pycmd是js中的函数
        self.web.stdHtml((self._body + self._add_word_body) % dict(
            tree=tree, stats=stats, models=models, countwarn=self._countWarn()),
                         css=["deckbrowser.css"],
                         js=["jquery.js", "jquery-ui.js", "deckbrowser.js", "add_words.js"])
        self.web.key = "deckBrowser"
        # 设置牌组浏览的下面三个button
        self._drawButtons()
        if offset is not None:
            self._scrollToOffset(offset)

    def _scrollToOffset(self, offset):
        self.web.eval("$(function() { window.scrollTo(0, %d, 'instant'); });" % offset)

    def _renderModels(self):
        # 加载页面的时候自动加载下拉框内容
        model_names = self.mw.col.models.allImportNames()
        current_name = self.mw.col.models.current().get('name')
        item_template = '<option value ="%s">%s</option>\n'
        select_template = '<option value=%s selected="selected">%s</option>'
        res = ''
        for name in reversed(model_names):
            if name != current_name:
                res += item_template % (name, name)
            else:
                res += select_template % (name, name)
        return res

    def _renderStats(self):
        cards, thetime = self.mw.col.db.first("""
select count(), sum(time)/1000 from revlog
where id > ?""", (self.mw.col.sched.dayCutoff - 86400) * 1000)
        cards = cards or 0
        thetime = thetime or 0
        msgp1 = ngettext("<!--studied-->%d card", "<!--studied-->%d cards", cards) % cards
        buf = _("Studied %(a)s %(b)s today.") % dict(a=msgp1,
                                                     b=fmtTimeSpan(thetime, unit=1, inTime=True))
        return buf

    def _countWarn(self):
        if (self.mw.col.decks.count() < 25 or
                self.mw.pm.profile.get("hideDeckLotsMsg")):
            return ""
        return "<br><div style='width:50%;border: 1px solid #000;padding:5px;'>" + (
                _("You have a lot of decks. Please see %(a)s. %(b)s") % dict(
            a=("<a href=# onclick=\"return pycmd('lots')\">%s</a>" % _(
                "this page")),
            b=("<br><small><a href=# onclick='return pycmd(\"hidelots\")'>("
               "%s)</a></small>" % (_("hide")) +
               "</div>")))

    def _renderDeckTree(self, nodes, depth=0):
        if not nodes:
            return ""
        if depth == 0:
            buf = """
<tr><th colspan=5 align=left>%s</th><th class=count>%s</th>
<th class=count>%s</th><th class=optscol></th></tr>""" % (
                _("Deck"), _("Due"), _("New"))
            buf += self._topLevelDragRow()
        else:
            buf = ""
        nameMap = self.mw.col.decks.nameMap()
        for node in nodes:
            buf += self._deckRow(node, depth, len(nodes), nameMap)
        if depth == 0:
            buf += self._topLevelDragRow()
        return buf

    def _deckRow(self, node, depth, cnt, nameMap):
        name, did, due, lrn, new, children = node
        deck = self.mw.col.decks.get(did)
        if did == 1 and cnt > 1 and not children:
            # if the default deck is empty, hide it
            if not self.mw.col.db.scalar("select 1 from cards where did = 1"):
                return ""
        # parent toggled for collapsing
        for parent in self.mw.col.decks.parents(did, nameMap):
            if parent['collapsed']:
                buff = ""
                return buff
        prefix = "-"
        if self.mw.col.decks.get(did)['collapsed']:
            prefix = "+"
        due += lrn

        def indent():
            return "&nbsp;" * 6 * depth

        if did == self.mw.col.conf['curDeck']:
            klass = 'deck current'
        else:
            klass = 'deck'
        buf = "<tr class='%s' id='%d'>" % (klass, did)
        # deck link
        if children:
            collapse = "<a class=collapse href=# onclick='return pycmd(\"collapse:%d\")'>%s</a>" % (did, prefix)
        else:
            collapse = "<span class=collapse></span>"
        if deck['dyn']:
            extraclass = "filtered"
        else:
            extraclass = ""
        buf += """

        <td class=decktd colspan=5>%s%s<a class="deck %s"
        href=# onclick="return pycmd('open:%d')">%s</a></td>""" % (
            indent(), collapse, extraclass, did, name)

        # due counts
        def nonzeroColour(cnt, colour):
            if not cnt:
                colour = "#e0e0e0"
            if cnt >= 1000:
                cnt = "1000+"
            return "<font color='%s'>%s</font>" % (colour, cnt)

        buf += "<td align=right>%s</td><td align=right>%s</td>" % (
            nonzeroColour(due, "#007700"),
            nonzeroColour(new, "#000099"))
        # options
        buf += ("<td align=center class=opts><a onclick='return pycmd(\"opts:%d\");'>"
                "<img src='/_anki/imgs/gears.svg' class=gears></a></td></tr>" % did)
        # children
        buf += self._renderDeckTree(children, depth + 1)
        return buf

    def _topLevelDragRow(self):
        return "<tr class='top-level-drag-row'><td colspan='6'>&nbsp;</td></tr>"

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
        source = self.mw.col.models.getCurrentSource()
        if not source:
            messageBox = QMessageBox()
            # 只有导入的模板才带有source
            messageBox.setText("未指定导入模板!")
            messageBox.exec_()
            return

        # 这个模板所需要的所有来源 ex: ['Baicizhan', 'Youdao']
        source_list = []
        for key, val in source.items():
            source_name = val.split(':')[0]
            if source_name not in source_list:
                source_list.append(source_name)

        words = content.strip().split('\n')
        index = 0
        # 保证了添加单词的顺序，且剔除空格
        while True:
            cnt = index
            if index == len(words):
                break
            if " " in words[index]:
                for tmp in words[index].split(' '):
                    if tmp != "":
                        words.insert(cnt + 1, tmp)
                        cnt = cnt + 1
                del words[index]
                index = cnt
            else:
                index = index + 1
        # 单词去重
        duplicate_words = {}
        errormsg = {}

        for i in words:
            if i in duplicate_words.keys():
                duplicate_words[i] += 1
            else:
                duplicate_words[i] = 1
        words_temp = []
        for i in duplicate_words.keys():
            words_temp.append(i)
            if duplicate_words[i] != 1:
                errormsg[i] = -3

        words = []
        note = self.mw.col.newNote()
        for i in words_temp:
            if note.newDupeOrEmpty(i) != 2:
                words.append(i)
            else:
                errormsg[i] = -3
        
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

        success_num = self.add_words(word_infos)
        report_add_res(len(words), success_num, errormsg)

    def _add_from_text(self, content):
        """

        :param content: textarea中的内容
        :return:
        """
        if not content:
            return

        self.__add_words_by_content(content)

    def _add_from_file(self):
        file_path = QFileDialog.getOpenFileName(None, '选择文件', './', "txt (*.txt)")[0]

        if not file_path:
            return

        messageBos = QMessageBox()
        if file_path.endswith('txt'):
            with open(file_path, 'r') as f:
                content = f.read()
            self.__add_words_by_content(content)
        else:
            messageBos.setText("必须是txt文件!")
            messageBos.exec_()

    def add_words(self, word_infos: list):
        r"""
        把从服务器得到的单词批量加入牌组
        :param word_infos:
        :return: 成功的个数
        """
        success_num = 0

        progress = QProgressDialog()
        progress.setWindowTitle("请稍等")
        progress.setLabelText("正在添加单词...")
        progress.setCancelButtonText("取消")
        progress.setMinimumDuration(500)
        progress.setWindowModality(Qt.WindowModal)
        progress.setRange(0, 100)
        progress.setValue(0)

        source_list = self.mw.col.models.getCurrentSource()

        addCard = self.mw.onAddCard(hidden=True)
        for idx, word_info in enumerate(word_infos):
            # 这个单词是否添加成功
            flag = 1
            word = None
            for cnt, flds in enumerate(addCard.editor.note._model['flds']):
                # 读取当前model的字段，根据当前字段将word_info内容添加进去
                try:
                    flds_name = flds['name']
                    source = source_list[flds_name]
                    key1, key2 = source.split(':')
                    # print(word_info[key1][key2])
                    # 判断word_info中是否有对应的field，若没有，则置为None
                    if key1 in word_info and key2 in word_info[key1]:
                        addCard.editor.note.fields[cnt] = word_info[key1][key2]
                    else:
                        addCard.editor.note.fields[cnt] = ''
                        continue

                    if key2 in ['word']:
                        word = word_info[key1][key2]
                    elif key2 in ['img']:
                        res = requests.get(word_info[key1][key2])
                        if not os.path.isdir("./images"):
                            os.mkdir("./images")
                        with open("./{}.jpg".format(word), "wb") as f:
                            f.write(res.content)
                        addCard.editor.note.fields[cnt] = "./{}.jpg".format(word)
                    elif key2 in ['sound']:
                        res = requests.get(word_info[key1][key2])
                        if not os.path.isdir("./sound"):
                            os.mkdir("./sound")
                        with open("./{}.mp3".format(word), "wb") as f:
                            f.write(res.content)
                        addCard.editor.note.fields[cnt] = "[sound:./{}.mp3]".format(word)
                except Exception as e:
                    flag = 0
                    print(e)
                    break

            success_num += flag
            print(addCard.editor.note.fields)
            addCard.addCards_hidden()

            if idx + 1 == len(word_infos):
                progress.setLabelText("添加完成")
            progress.setValue(int((idx + 1) * 100 / len(word_infos)))

        addCard.close_hidden()

        return success_num

    # 导入model
    ##########################################################################
    def __check_json(self, model_json, must_include=None):
        """
        检测json格式
        :param model_json: json
        :param must_include: 待检测的json中的键值
        :return:
        """
        if not must_include:
            must_include = ['name', 'fileds', 'template', 'source']

        for item in must_include:
            if item not in model_json:
                return False
            if item == 'template':
                return self.__check_json(model_json['template'], ['name', 'qfmt', 'afmt'])
        return True

    def __check_modelfield(self, model_json):
        # 检查导入模板source的字段键值是否标准
        # 注意这里的当前路径是Anki2下面的，而不是anki
        file_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../../..")), "stdfield.json")

        with open(file_path, 'r', encoding='utf8') as f:
            stdfield = json.load(f)
            for fld in model_json['source']:
                fld_source = model_json['source'][fld].split(":")[0]
                fld_name = model_json['source'][fld].split(":")[1]
                if fld_name not in stdfield[fld_source]:
                    return False
        return True

    def __import_json(self, content_json: dict):
        if not (self.__check_json(content_json) and self.__check_modelfield(content_json)):
            messageBos = QMessageBox()
            messageBos.setText("json文件模板格式错误!")
            messageBos.exec_()
            return None

        mm = self.mw.col.models
        m = mm.new(_(content_json['name']))
        for filed_name in content_json['fileds']:
            fm = mm.newField(_(filed_name))
            mm.addField(m, fm)

        t = mm.newTemplate(_(content_json['template']['name']))
        t['qfmt'] = content_json['template']['qfmt']
        t['afmt'] = content_json['template']['afmt']
        mm.addTemplate(m, t)

        mm.addSource(m, content_json['source'])

        mm.add(m)

        return m

    def _import_model(self):
        file_path = QFileDialog.getOpenFileName(None, '选择模板文件', './', "json (*.json)")[0]
        if not file_path:
            return

        messageBos = QMessageBox()
        if file_path.endswith('json'):
            with open(file_path, 'r', encoding='utf8') as f:
                content = json.load(f)
                res = self.__import_json(content)
                if res:
                    messageBos.setText("模板导入成功!")
                    messageBos.exec_()
        else:
            messageBos.setText("必须是json文件!")
            messageBos.exec_()

        # 导入新模板之后重新加载deckBrowser页面
        self.mw.moveToState("deckBrowser")

    # 导入model
    ##########################################################################
    def _change_model(self, model_name):
        m = self.mw.col.models.byName(model_name)
        self.mw.col.conf['curModel'] = m['id']
        cdeck = self.mw.col.decks.current()
        cdeck['mid'] = m['id']
        self.mw.col.decks.save(cdeck)
        runHook("currentModelChanged")
        self.mw.reset()

    # Options
    ##########################################################################
    def _showOptions(self, did):
        m = QMenu(self.mw)
        a = m.addAction(_("Rename"))
        a.triggered.connect(lambda b, did=did: self._rename(did))
        a = m.addAction(_("Options"))
        a.triggered.connect(lambda b, did=did: self._options(did))
        a = m.addAction(_("Export"))
        a.triggered.connect(lambda b, did=did: self._export(did))
        a = m.addAction(_("Delete"))
        a.triggered.connect(lambda b, did=did: self._delete(did))
        runHook("showDeckOptions", m, did)
        m.exec_(QCursor.pos())

    def _export(self, did):
        self.mw.onExport(did=did)

    def _rename(self, did):
        self.mw.checkpoint(_("Rename Deck"))
        deck = self.mw.col.decks.get(did)
        oldName = deck['name']
        newName = getOnlyText(_("New deck name:"), default=oldName)
        newName = newName.replace('"', "")
        if not newName or newName == oldName:
            return
        try:
            self.mw.col.decks.rename(deck, newName)
        except DeckRenameError as e:
            return showWarning(e.description)
        self.show()

    def _options(self, did):
        # select the deck first, because the dyn deck conf assumes the deck
        # we're editing is the current one
        self.mw.col.decks.select(did)
        self.mw.onDeckConf()

    def _collapse(self, did):
        self.mw.col.decks.collapse(did)
        self._renderPage(reuse=True)

    def _dragDeckOnto(self, draggedDeckDid, ontoDeckDid):
        try:
            self.mw.col.decks.renameForDragAndDrop(draggedDeckDid, ontoDeckDid)
        except DeckRenameError as e:
            return showWarning(e.description)

        self.show()

    def _delete(self, did):
        if str(did) == '1':
            return showWarning(_("The default deck can't be deleted."))
        self.mw.checkpoint(_("Delete Deck"))
        deck = self.mw.col.decks.get(did)
        if not deck['dyn']:
            dids = [did] + [r[1] for r in self.mw.col.decks.children(did)]
            cnt = self.mw.col.db.scalar(
                "select count() from cards where did in {0} or "
                "odid in {0}".format(ids2str(dids)))
            if cnt:
                extra = ngettext(" It has %d card.", " It has %d cards.", cnt) % cnt
            else:
                extra = None
        if deck['dyn'] or not extra or askUser(
                (_("Are you sure you wish to delete %s?") % deck['name']) +
                extra):
            self.mw.progress.start(immediate=True)
            self.mw.col.decks.rem(did, True)
            self.mw.progress.finish()
            self.show()

    # Top buttons
    ######################################################################

    drawLinks = [
        ["", "shared", _("Get Shared")],
        ["", "create", _("Create Deck")],
        ["Ctrl+I", "import", _("Import File")],  # Ctrl+I works from menu
    ]

    def _drawButtons(self):
        buf = ""
        drawLinks = deepcopy(self.drawLinks)
        for b in drawLinks:
            if b[0]:
                b[0] = _("Shortcut key: %s") % shortcut(b[0])
            buf += """
<button title='%s' onclick='pycmd(\"%s\");'>%s</button>""" % tuple(b)
        self.bottom.draw(buf)
        self.bottom.web.onBridgeCmd = self._linkHandler

    def _onShared(self):
        openLink(aqt.appShared + "decks/")
