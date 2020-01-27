# Copyright: Ankitects Pty Ltd and contributors
# -*- coding: utf-8 -*-
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

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
from get_word import report_add_res,MyThread
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
<div class="buttonbox">
    <div><textarea id="words-area"></textarea></div>
    <div>
        <table>
            <tr>
                <th><button type="button" id="add_from_text_bt">添加文本框中单词</button></th>
            </tr>
            <tr>
                <th><button type="button" id="add_from_file_bt">从文件导入单词</button></th>
            </tr>
            <tr>
                <th><button type="button" id="import_model">导入新的模板</button></th>
            </tr>
        </table>
    </div>
    </br>
    <label>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp请选择模板&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</label>
    <select>
        <option value="volvo">Volvo</option>
        <option value="saab">Saab</option>
        <option value="opel">Opel</option>
        <option value="audi">Audi</option>
    </select>
</div>
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
        # 点击html中的某个链接会返回一个类似于pycmd('open:1')的东西
        # 其中pycmd是js中的函数
        self.web.stdHtml((self._body + self._add_word_body) % dict(
            tree=tree, stats=stats, countwarn=self._countWarn()),
                         css=["deckbrowser.css"],
                         js=["jquery.js", "jquery-ui.js", "deckbrowser.js", "add_words.js"])
        self.web.key = "deckBrowser"
        # 设置牌组浏览的下面三个button
        self._drawButtons()
        if offset is not None:
            self._scrollToOffset(offset)

    def _scrollToOffset(self, offset):
        self.web.eval("$(function() { window.scrollTo(0, %d, 'instant'); });" % offset)

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
        messageBox = QMessageBox()

        words = content.strip().split('\n')
        word_infos = []
        # for word in words:
        #     info = get_word(word)
        #     if info and 'word' in info:
        #         word_infos.append(info)
        threads = []
        for i in range(len(words)):
            t = MyThread(words[i])
            t.start()
            threads.append(t)
        for i in range(len(threads)):
            threads[i].join()
            info = threads[i].get_result()
            word_infos.append(info)
        res_to_show = ""
        for info in word_infos:
            res_to_show += str(info) + '\n'

        messageBox.setText(res_to_show)
        messageBox.exec_()

        self.__add_words(word_infos)
        # self.words_text.setText("")

        report_add_res(len(words), len(word_infos))
        return words, word_infos

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

    def __add_words(self, word_infos: list):
        r"""
        把从服务器得到的单词批量加入牌组
        :param word_infos:
        :return:
        """
        for word_info in word_infos:
            addCard = self.mw.onAddCard(hidden=True)
            # 一开始有一个 '.'?
            # addCard.editor.note.fields.clear()
            addCard.editor.note.fields[0] = word_info['word']
            addCard.editor.note.fields[1] = word_info['accent']
            addCard.editor.note.fields[2] = word_info['mean_cn']
            addCard.editor.note.fields[3] = word_info['st']

            res = requests.get(word_info['img'])
            if not os.path.isdir("./images"):
                os.mkdir("./images")
            with open("./images/{}.jpg".format(word_info['word']), "wb") as f:
                f.write(res.content)
            addCard.editor.note.fields[4] = "./images/{}.jpg".format(word_info['word'])

            res = requests.get(word_info['sound'])
            if not os.path.isdir("./sound"):
                os.mkdir("./sound")
            with open("./sound/{}.mp3".format(word_info['word']), "wb") as f:
                f.write(res.content)
            addCard.editor.note.fields[5] = "[sound:./sound/{}.mp3]".format(word_info['word'])

            # print(os.getcwd())
            # addCard.editor.note.fields[4] = [res.content]

            print(addCard.editor.note.fields)
            # 直接调用_addCards， addCards涉及的函数太多了，暂时没法搞明白
            addCard._addCards()
            addCard.close()

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
            must_include = ['name', 'fileds', 'template']

        for item in must_include:
            if item not in model_json:
                return False
            if item == 'template':
                return self.__check_json(model_json['template'], ['name', 'qfmt', 'afmt'])
        return True

    def __import_json(self, content_json):
        if not self.__check_json(content_json):
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
        mm.add(m)

        return m

    def _import_model(self):
        file_path = QFileDialog.getOpenFileName(None, '选择模板文件', './', "json (*.json)")[0]
        if not file_path:
            return

        messageBos = QMessageBox()
        if file_path.endswith('json'):
            with open(file_path, 'r') as f:
                content = json.load(f)
                res = self.__import_json(content)
                if res:
                    messageBos.setText("模板导入成功!")
                    messageBos.exec_()
        else:
            messageBos.setText("必须是json文件!")
            messageBos.exec_()

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
