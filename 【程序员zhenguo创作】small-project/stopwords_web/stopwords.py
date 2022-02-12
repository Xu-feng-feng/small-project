import os
from collections import OrderedDict
from util import eng2chi

from pypinyin import lazy_pinyin


def do_stopwords():
    result_dict = dict()
    Result = type('Result', (object,), dict(word_n=0, words=list()))
    try:
        for file in os.listdir('stopwords'):
            if file == '.DS_Store':
                continue
            res = Result()
            file_path = os.path.join('stopwords', file)
            with open(file_path) as fr:
                stopwords = fr.readlines()
                res.word_n = len(stopwords)
                res.words = ','.join(map(lambda word: word.replace('\n', ''), stopwords[:5]))
                result_dict[eng2chi[file]] = res

        return OrderedDict(sorted(result_dict.items(), key=lambda x: lazy_pinyin(x[0])))
    except FileNotFoundError as no_found:
        raise no_found
