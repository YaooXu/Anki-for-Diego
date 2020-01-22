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
3. Editor.saveNow调用AnkiWebView.evalWithCallback(lambda: AddCards._addCards)
4. 将动作加入到动作队列AnkiWebView._pendingActions
5. AnkiWebView._maybeRunActions尝试执行队列中的任务
6. _evalWithCallback?

- **实现思路**

1. 在主界面点击查询单词按钮后，**隐式**创建AddCards页面，并把得到的单词信息手动添加到AddCards.Editor.note.fields中，然后调用AddCards.addCards

- ~~bug~~

1. ~~AddCards.Editor.note.fields的内容在AddCards._addNotes中发生了改变，第一个元素变为空，导致添加失败，报错“first field is empty"~~

   **SOLVE：调用AddCards._addCards**，addCards涉及的函数太多了，暂时没法搞明白


#### 添加Note Type

- **流程**
 1. 在工具栏点击Tools，选择Manage Note Types 或者在addcards中选择marge type，调用aqt\main.py下的onNoteTypes函数；
 2. 进入aqt\models.py创建一个models对象（界面），展示Note Types界面，右边栏包括：Add、Rename、Delete等操作；
 3. 点击Add，调用aqt\models.py下的onAdd()函数，创建一个AddModel()对象，AddModel类定义在aqt\models.py里面；
 4. 创建AddModel对象时，读取anki\stdmodels中预置的标准Note Type，共五种：BasicModel、BasicTypingModel、ForwardReverse、ForwardOptionalReverse、ClozeModel，读取预置model之后，将这五种model再copy一遍，共十种model；
 5. 在添加Note Type界面中给出的十种model中选择一种作为新的model，命名，保存新的model，然后调用updateModelsList()方法，重新加载，完成Note Type整个添加流程。



## TODO

> 按优先级排列

- 修复添加卡片的bug
- 实现anki默认牌组，默认卡片模板
- UI进行整合，看能不能兼容
- PC文档详细化（模块运行流程图、文件夹作用，主要类的作用）

- UI美化（把添加单词那块的间距和button调一下）

### Type默认配置的加载
1. 程序启动 调用 **anki\storage.py** 中的 `Collection` 函数  `Collection` 接收一个核心参数path <br>
2. path理解为保存数据库的路径，若第一次调用即无数据库，那么就使用默认配置生成一个数据库 <br>
3. 关于Type的默认配置的生成 系统会调用 **anki\stdmodels.py** 中的 几个函数`addBasicModel`，`addBasicTypingModel`，`addForwardReverse`，`addForwardOptionalReverse`，`addClozeModel`