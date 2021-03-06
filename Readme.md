# ANKI 文档分析
## 文件夹作用
### aqt
- forms 
  
    由.ui文件通过build_ui.sh生成的前端.py代码
    
- **TODO**

## 部分核心功能流程及实现方式
### 卡片添加相关

#### 添加卡片

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

#### 选择model和template

1. 在AddCards类初始化的时候调用setupChoosers函数，该函数设置AddCards上面的选择model和deck。
2. 生成aqt.modelchooser.ModelChooser和aqt.deckchooser.DeckChooser两个类，分别负责选择model和deck。
3. 以选择model为例。ModelChooser的初始化中会调用setupModels函数来加载那一小块的页面，并把按钮点击信号连接到onModelChange函数。
4. 当点击按钮，调用onModelChange函数，该函数中构造StudyDeck类，该类可以通过传入的参数加载多种选择列表，这里加载的是model的选择列表。
5. 当选中choose note type中的model，触发StudyDeck的accept函数，并把当前选中的model的name赋值给self.name,Qdialog调用accept方法关闭model选择页面。
6. choose note type页面关闭后，onModelChange继续运行，检测StudyDeck类中的name是否非空，如果非空则说明在上一页面选择了model。若非空，通过model名称得到model信息，并设置为当前model（self.deck.conf['curModel']）


### 添加Note Type

- **流程**
 1. 在工具栏点击Tools，选择Manage Note Types 或者在addcards中选择marge type，调用aqt\main.py下的onNoteTypes函数；
 2. 进入aqt\models.py创建一个models对象（界面），展示Note Types界面，右边栏包括：Add、Rename、Delete等操作；
 3. 点击Add，调用aqt\models.py下的onAdd()函数，创建一个AddModel()对象，AddModel类定义在aqt\models.py里面；
 4. 创建AddModel对象时，读取anki\stdmodels中预置的标准Note Type，共五种：BasicModel、BasicTypingModel、ForwardReverse、ForwardOptionalReverse、ClozeModel，读取预置model之后，将这五种model再copy一遍，共十种model；
 5. 在添加Note Type界面中给出的十种model中选择一种作为新的model，命名，保存新的model，然后调用updateModelsList()方法，重新加载，完成Note Type整个添加流程。

#### 修改字段fields
- **流程**
 1. 点击Add之后进入添加单词界面，点击Fields...，注意此时修改字段是修改对应的Note Type，即model，调用aqt\editor.py的onFields函数，进而调用self._onFields私有方法，进入修改字段页面；
 2. 创建一个FieldDialog对象，该类定义在apt\fields.py文件中，具体函数有Add、Delete、Rename等，修改的都是当前model；
 3. 以Add为例，调用onAdd方法，输入新field的name，先调用self.saveField()（先保存？），然后调用anki\models.py文件下的newField()方法，创建新的field，命名为输入的name；
 4. 之后调用anki\models.py文件下的addField()方法，将新的field添加到当前的model中，重新加载，完成add流程；

#### 删除卡片

- **流程**
1. 点击主界面的Browse按钮，创建一个browser对象，在对应deck中找到想删除的卡片，鼠标右键创建一个Qmune对象，点击delete进行删除
2. 删除时调用deleteNotes方法，进而调用_deleteNotes开始删除，首先定位当前的行数，注意这里是可以一次选中多行，多个卡片同时进行删除的
3. 读取选中的行数中单词在数据库中对应的id，具体方法调用browser.selectedNotes方法，查询db中卡片id，返回值赋值给名为nids的一个list
4. 然后调用collection中的remNote方法，从数据库中删除对应的card
5. 删除之后根据删掉的行数重新加载整个页面

### 数据库相关操作

#### 初始化

1. 在aqt/main.py的setupProfile中调用loadProfile，再调用loadCollection
2. 尝试调用_loadCollection，再调用anki/storage.Collection函数，在该函数中完成数据库的初始化工作，并创建 _Collection类（该类是数据库的接口，提供model，decks等内容的管理类，同时创建这个类的时候会调用load函数从数据库中把所有的models、deck、conf加载），如果是新创建的用户则还需要使用stdmodels中的模板生成函数生成标准模板。

### 音频播放相关操作

#### 关于卡片音频如何播放

1. 在aqt\reviewer.py中，有函数_showQuestion，这个函数在点击显示答案按钮之后调用anki\sound.py中的playFromText函数，在playFromText函数中，调用anki\sound.py中allSounds从显示答案的html中匹配出音频，匹配正则为`r"\[sound:(.*?)\]"`，所以有关音频的字段应以这个正则形式保存，playFromText将所有匹配出的音频交付给playsound进行播放

#### 录音流程及播放

1. 点击录音按钮后，调用aqt\reviewer.py中的onRecordVoice函数，该函数内首先调用aqt\sound.py中的getAudio函数，该函数内实例化一个anki\sound.py中的PyAudioRecorder类，该类内实例一个PyAudioThreadedRecorder多线程录音类，在getAudio中完成多线程录音操作(录音及保存的具体实现在PyAudioThreadedRecorder类中)。录音的播放使用aqt\reviewer.py中的onReplayRecorded函数，调用playsound进行播放

#### 关于playsound的修改

1. playsound库在播放音频后，不会收回对文件的控制，此时其他代码需要更改音频则会失败(多次录音),需要对playsound进行修改，在playsound.py中`winCommand`函数内添加如下

```python
        winCommand('play', alias, 'from 0 to', durationInMS.decode())

    while True:
        if winCommand('status', alias, 'mode').decode() == 'stopped':
            winCommand('close', alias)
            break
```

### 选择卡片model

#### 下拉框加载

​	下拉框中的所有模型名称均在deckbroswer页面加载的过程中加载，具体函数为deckbroswer._renderModels，加载完之后便无法动态变更，因此导入新模板之后为了更新下拉框内容，需要重新加载一次deckbrowser页面。

#### 模板改变

​	当改变下拉框中内容时，触发js中的函数，把改变之后的内容返回给python，再在python中实现默认模板变更。

### 爬取单词进度条的实现

整个实现流程相对比较复杂，对于一些原来的函数也有所修改

总体运行流程为：

- 创建线程列表threads每个线程爬取一个单词
- 将线程列表传入进度条类mybar
- mybar调用worker类传入线程列表threads进行爬取
- worker类执行完每个进程后更新mybar的进度条

为了方便查看我在爬取的是我设置了爬完一个停1秒方便发现错误

还有一个问题就是我发现单词卡会重复，如果他有这个单词依然会重复添加，不知道这个需不需要处理

## TODO

> 按优先级排列
> - PC测试
>   - 添加, 删除卡片
>   - 导入, 删除模板
>   - 智能添加
>- 安卓测试
>   - 添加, 删除单词
>- 同步测试