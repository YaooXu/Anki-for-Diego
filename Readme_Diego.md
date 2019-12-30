# ANKI 文档分析
## 文件夹作用
### aqt
- forms 
    
    由.ui文件通过build_ui.sh生成的前端.py代码
    
- **TODO**

## 部分核心功能流程及实现方式
### 卡片添加

- **流程**

       1. 点击add， 打开AddCards Dialog同时创建Editor对象在AddCards页面中填写内容，此时填写的内容均保存在Editor对象中,具体保存在Editor.note.fields（list)中
          2. 点击添加，调用AddCards.addCards，该方法同时调用Editor.saveNow和AddCards._addCards
          3. 后续会调用addNotes和回调函数，具体作用暂不明确 

- **实现思路**

1. 在主界面点击查询单词按钮后，**隐式**创建AddCards页面，并把得到的单词信息手动添加到AddCards.Editor.note.fields中，然后调用AddCards.addCards

- bug

1. AddCards.Editor.note.fields的内容在AddCards._addNotes中发生了改变，第一个元素变为空，导致添加失败，报错“first field is empty"

## TODO

> 按优先级排列

- 修复添加卡片的bug
- 实现anki默认牌组，默认卡片模板
- UI进行整合，看能不能兼容
- PC文档详细化（模块运行流程图、文件夹作用，主要类的作用）

- UI美化（把添加单词那块的间距和button调一下）