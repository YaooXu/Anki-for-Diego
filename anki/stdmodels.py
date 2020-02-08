# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from anki.lang import _
from anki.consts import MODEL_CLOZE

models = []


# Basic
##########################################################################

def addBasicModel(col):
    # 默认的单词模板
    # ModelManager
    mm = col.models
    m = mm.new("默认单词模板")
    fm = mm.newField("单词")
    mm.addField(m, fm)
    fm = mm.newField("音标")
    mm.addField(m, fm)
    fm = mm.newField("释义")
    mm.addField(m, fm)
    fm = mm.newField("例句")
    mm.addField(m, fm)
    fm = mm.newField("图片")
    mm.addField(m, fm)
    fm = mm.newField("音频")
    mm.addField(m, fm)

    t = mm.newTemplate("默认显示样式")
    t['qfmt'] = "{{单词}}<br>{{音标}}<span class='voice'>{{音频}}</span>"
    t['afmt'] = "{{FrontSide}}\n\n<hr id=answer>\n\n{{释义}}<br>{{例句}}<br><img src={{图片}} alt=\"图片\">"
    mm.addTemplate(m, t)

    source = {
        "单词": "Baicizhan:word",
        "音标": "Baicizhan:accent",
        "释义": "Baicizhan:mean_cn",
        "例句": "Youdao:explains",
        "图片": "Baicizhan:img",
        "音频": "Youdao:sound"
    }
    mm.addSource(m, source)
    mm.add(m)

    return m


models.append((lambda: _("Basic"), addBasicModel))

# Basic w/ typing
##########################################################################
