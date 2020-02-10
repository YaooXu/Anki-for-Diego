from __future__ import print_function
import sys
import time
import os
import io
import csv
import sqlite3
import codecs

try:
    import json
except:
    import simplejson as json

MySQLdb = None


#----------------------------------------------------------------------
# python3 compatible
#----------------------------------------------------------------------
if sys.version_info[0] >= 3:
    unicode = str
    long = int
    xrange = range

def stripword(word):
    return (''.join([ n for n in word if n.isalnum() ])).lower()

class StarDict (object):

    def __init__ (self, filename, verbose = False):
        self.__dbname = filename
        if filename != ':memory:':
            os.path.abspath(filename)
        self.__conn = None
        self.__verbose = verbose
        self.__open()

    # 初始化并创建必要的表格和索引
    def __open (self):
        sql = '''
        CREATE TABLE IF NOT EXISTS "stardict" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            "word" VARCHAR(64) COLLATE NOCASE NOT NULL UNIQUE,
            "sw" VARCHAR(64) COLLATE NOCASE NOT NULL,
            "phonetic" VARCHAR(64),
            "definition" TEXT,
            "translation" TEXT,
            "pos" VARCHAR(16),
            "collins" INTEGER DEFAULT(0),
            "oxford" INTEGER DEFAULT(0),
            "tag" VARCHAR(64),
            "bnc" INTEGER DEFAULT(NULL),
            "frq" INTEGER DEFAULT(NULL),
            "exchange" TEXT,
            "detail" TEXT,
            "audio" TEXT
        );
        CREATE UNIQUE INDEX IF NOT EXISTS "stardict_1" ON stardict (id);
        CREATE UNIQUE INDEX IF NOT EXISTS "stardict_2" ON stardict (word);
        CREATE INDEX IF NOT EXISTS "stardict_3" ON stardict (sw, word collate nocase);
        CREATE INDEX IF NOT EXISTS "sd_1" ON stardict (word collate nocase);
        '''

        self.__conn = sqlite3.connect(self.__dbname, isolation_level = "IMMEDIATE")
        self.__conn.isolation_level = "IMMEDIATE"

        sql = '\n'.join([ n.strip('\t') for n in sql.split('\n') ])
        sql = sql.strip('\n')

        self.__conn.executescript(sql)
        self.__conn.commit()

        fields = ( 'id', 'word', 'sw', 'phonetic', 'definition', 
            'translation', 'pos', 'collins', 'oxford', 'tag', 'bnc', 'frq', 
            'exchange', 'detail', 'audio' )
        self.__fields = tuple([(fields[i], i) for i in range(len(fields))])
        self.__names = { }
        for k, v in self.__fields:
            self.__names[k] = v
        self.__enable = self.__fields[3:]
        return True

    # 数据库记录转化为字典
    def __record2obj (self, record):
        if record is None:
            return None
        word = {}
        for k, v in self.__fields:
            word[k] = record[v]
        if word['detail']:
            text = word['detail']
            try:
                obj = json.loads(text)
            except:
                obj = None
            word['detail'] = obj
        return word

    # 关闭数据库
    def close (self):
        if self.__conn:
            self.__conn.close()
        self.__conn = None
    
    def __del__ (self):
        self.close()

    # 输出日志
    def out (self, text):
        if self.__verbose:
            print(text)
        return True

    # 查询单词
    def query (self, key):
        c = self.__conn.cursor()
        record = None
        if isinstance(key, int) or isinstance(key, long):
            c.execute('select * from stardict where id = ?;', (key,))
        elif isinstance(key, str) or isinstance(key, unicode):
            c.execute('select * from stardict where word = ?', (key,))
        else:
            return None
        record = c.fetchone()
        return self.__record2obj(record)
    
    def tag(self,key):
        c = self.__conn.cursor()
        record = None
        if isinstance(key, int) or isinstance(key, long):
            c.execute('select tag from stardict where id = ?;', (key,))
        elif isinstance(key, str) or isinstance(key, unicode):
            c.execute('select tag from stardict where word = ?', (key,))
        else:
            return None
        record = c.fetchone()
        return record
    # 查询单词匹配
    def match (self, word, limit = 10, strip = False):
        c = self.__conn.cursor()
        if not strip:
            sql = 'select id, word from stardict where word >= ? '
            sql += 'order by word collate nocase limit ?;'
            c.execute(sql, (word, limit))
        else:
            sql = 'select id, word from stardict where sw >= ? '
            sql += 'order by sw, word collate nocase limit ?;'
            c.execute(sql, (stripword(word), limit))
        records = c.fetchall()
        result = []
        for record in records:
            result.append(tuple(record))
        return result

    # 批量查询
    def query_batch (self, keys):
        sql = 'select * from stardict where '
        if keys is None:
            return None
        if not keys:
            return []
        querys = []
        for key in keys:
            if isinstance(key, int) or isinstance(key, long):
                querys.append('id = ?')
            elif key is not None:
                querys.append('word = ?')
        sql = sql + ' or '.join(querys) + ';'
        query_word = {}
        query_id = {}
        c = self.__conn.cursor()
        c.execute(sql, tuple(keys))
        for row in c:
            obj = self.__record2obj(row)
            query_word[obj['word'].lower()] = obj
            query_id[obj['id']] = obj
        results = []
        for key in keys:
            if isinstance(key, int) or isinstance(key, long):
                results.append(query_id.get(key, None))
            elif key is not None:
                results.append(query_word.get(key.lower(), None))
            else:
                results.append(None)
        return tuple(results)

    # 取得单词总数
    def count (self):
        c = self.__conn.cursor()
        c.execute('select count(*) from stardict;')
        record = c.fetchone()
        return record[0]

    # 注册新单词
    def register (self, word, items, commit = True):
        sql = 'INSERT INTO stardict(word, sw) VALUES(?, ?);'
        try:
            self.__conn.execute(sql, (word, stripword(word)))
        except sqlite3.IntegrityError as e:
            self.out(str(e))
            return False
        except sqlite3.Error as e:
            self.out(str(e))
            return False
        self.update(word, items, commit)
        return True

    # 删除单词
    def remove (self, key, commit = True):
        if isinstance(key, int) or isinstance(key, long):
            sql = 'DELETE FROM stardict WHERE id=?;'
        else:
            sql = 'DELETE FROM stardict WHERE word=?;'
        try:
            self.__conn.execute(sql, (key,))
            if commit:
                self.__conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    # 清空数据库
    def delete_all (self, reset_id = False):
        sql1 = 'DELETE FROM stardict;'
        sql2 = "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'stardict';"
        try:
            self.__conn.execute(sql1)
            if reset_id:
                self.__conn.execute(sql2)
            self.__conn.commit()
        except sqlite3.IntegrityError as e:
            self.out(str(e))
            return False
        except sqlite3.Error as e:
            self.out(str(e))
            return False
        return True

    # 更新单词数据
    def update (self, key, items, commit = True):
        names = []
        values = []
        for name, id in self.__enable:
            if name in items:
                names.append(name)
                value = items[name]
                if name == 'detail':
                    if value is not None:
                        value = json.dumps(value, ensure_ascii = False)
                values.append(value)
        if len(names) == 0:
            if commit:
                try:
                    self.__conn.commit()
                except sqlite3.IntegrityError:
                    return False
            return False
        sql = 'UPDATE stardict SET ' + ', '.join(['%s=?'%n for n in names])
        if isinstance(key, str) or isinstance(key, unicode):
            sql += ' WHERE word=?;'
        else:
            sql += ' WHERE id=?;'
        try:
            self.__conn.execute(sql, tuple(values + [key]))
            if commit:
                self.__conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    # 浏览词典
    def __iter__ (self):
        c = self.__conn.cursor()
        sql = 'select "id", "word" from "stardict"'
        sql += ' order by "word" collate nocase;'
        c.execute(sql)
        return c.__iter__()

    # 取得长度
    def __len__ (self):
        return self.count()

    # 检测存在
    def __contains__ (self, key):
        return self.query(key) is not None

    # 查询单词
    def __getitem__ (self, key):
        return self.query(key)

    # 提交变更
    def commit (self):
        try:
            self.__conn.commit()
        except sqlite3.IntegrityError:
            self.__conn.rollback()
            return False
        return True

    # 取得所有单词
    def dumps (self):
        return [ n for _, n in self.__iter__() ]
