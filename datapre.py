#!/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import re
import os
# MY_WORK_SPACE = os.environ['MY_WORK_SPACE']
# sys.path.append(MY_WORK_SPACE)
# from keywords.tokenizer_handler import TokenizerHandler
# from util.str_util import filter_html_tag
import jieba,string

class Data_pre():  
    def __init__(self):  
        # self.tk = TokenizerHandler()
        self.filter_punc = None

    def contain_zh(self,word):
        """判断字符串是否包含中文"""
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        word = word.decode()
        match = zh_pattern.search(word)
        return match

    # 结巴分词
    def wordSegJieba(self, sentence):
        seg_list = jieba.cut(sentence, cut_all=False)
        return seg_list  # 返回迭代器

    def content_to_list(self,sentence,filter_punc=True,filter_html=True,filter_num=False):
        sentence = re.sub(r'\s+', r' ', sentence) #将空白全部替换为' '
        sentence = sentence.replace('\n', ' ')
        words_list = self.wordSegJieba(sentence)
        res = []
        for w in words_list:
            try:w.decode('utf8')
            except:continue
            if filter_punc:  # 删除标点符号
                punc_words = [x for x in string.punctuation if x not in ['-', "'"]]  #所有英文标点
                if w in punc_words:continue
                if (not w.isdigit()) and (not w.isalpha()) and (not self.contain_zh(w)):  #非中文、数字、字母
                    continue
            try:
                word = w.decode('utf8')
                res.append(word)
            except:
                continue
        return res

            
if __name__=="__main__":
    dp = Data_pre()
    content = '陈鲁豫粉裙现身变“小公举” 一路微笑女人味十足'
    res = dp.content_to_list(content)
    res = ' '.join(res)
    print res

    '''
        def content_to_list(self,sentence,filter_punc=True,filter_html=True,filter_num=False):
            sentence = re.sub(r'\s+', r' ', sentence)
            sentence = sentence.replace('\n',' ')
            if filter_html:   #过滤HTML标签
                sentence = filter_html_tag(sentence)
            if filter_num:
                r1 = "[\u4e00-\u9fa5]+"
                sentence = re.sub(r1, ' number ', sentence)
            words_dic = self.tk.split(sentence)
            res = []
            r2 = u'[’!"#,.!?:;~，。！？√：；～$%&\'()*+,-./:;<=>?@，。?★、…【】◆：×％■③●—（）；·《》～？“”‘’﹔！[\\]^_`{|}~]'
            for w in words_dic:
                try:a = w['word'].decode('utf8')
                except:continue
                if filter_punc:      #删除标点符号
                    if w['pos_tag'] == 25:
                        re.sub(r2,' ',w['word'])
                        w['word'] = ' '
                    #if (not w['word'].isdigit()) and (not w['word'].isalpha()) and (unicode(w['word'])<u'\u4e00'or unicode(w['word'])>u'\u9fff'):  #非中文、数字、字母
                    if (not w['word'].isdigit()) and (not w['word'].isalpha()) and (not self.contain_zh(w['word'])):
                        w['word'] = ' '
                word = w['word']
                try:
                    word = word.decode('utf8')
                    res.append(word)
                except:continue
            return res
            '''

