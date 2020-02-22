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
    m = mm.new("Diego爸爸定制模板")
    fm = mm.newField("单词")
    mm.addField(m, fm)
    fm = mm.newField("释义")
    mm.addField(m, fm)
    fm = mm.newField("例句")
    mm.addField(m, fm)
    fm = mm.newField("图片")
    mm.addField(m, fm)
    fm = mm.newField("音频")
    mm.addField(m, fm)

    t = mm.newTemplate("Diego爸爸定制显示样式")
    t['qfmt'] = "{{单词}}<br><span class='voice'>{{音频}}</span>"
    t['afmt'] = "{{FrontSide}}\n\n<hr id=answer>{{例句}}<br>{{图片}}<br>{{释义}}"
    mm.addTemplate(m, t)

    source = {
        "单词": "Baicizhan:word",
        "释义": "Baicizhan:mean_cn",
        "例句": "Baicizhan:st",
        "图片": "Baicizhan:img",
        "音频": "Baicizhan:sound"
    }
    mm.addSource(m, source)
    mm.add(m)

    return m


models.append((lambda: _("Basic"), addBasicModel))

# Basic w/ typing
##########################################################################
