import requests
import json

headers = {
    'Content-Type': 'application/json'
}  # 定义头文件，伪装成浏览器
url = 'http://39.107.105.182:9999/getword'


def get_word(word, timeout=5):
    r"""

    :param word: 需要查询的单词
    :param timeout: 时间限制
    :return: 如果查询成功，返回该单词的信息的字典，否则返回None
    {
        "word": 单词 str
        "accent": 音标 str
        "sound": 发音的链接 str
        "mean_cn": 中文释义 str
        "img": 图片的网页链接 str
        "st":例句 str
        "sttr":例句翻译 str
    }
    """
    data = {'fastq': word}
    response = requests.post(url, data=json.dumps(data), headers=headers, timeout=timeout)
    if response.status_code == 200:
        word_info = response.json()
        return word_info
    else:
        return None


if __name__ == '__main__':
    word_info = get_word('test')
