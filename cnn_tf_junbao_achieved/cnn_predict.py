#!/data0/home/junbao/anaconda2/bin/python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import predict_longText
import ModelLoader_longText
import json
import math
import time
import datetime

MY_WORK_SPACE = os.environ['MY_WORK_SPACE']
sys.path.append(MY_WORK_SPACE)
from keywords.tokenizer_handler import *
MY_DIRECTORY = os.environ['MY_DIRECTORY']
sys.path.append(MY_DIRECTORY)
from datapre import *
dp = Data_pre()

ISOTIMEFORMAT='%Y-%m-%d %X'

class CNNClassify:
    #def __init__(self, vocabulary_inv, vocabulary_invmap,cnn_model, labels, classify, bayes_model,hot_top_map, stopword_dict,tagword_dict,cateIdName):

    def __init__(self):
        self.model = ModelLoader_longText.ModelLoader()
        self.vocabulary_inv = self.model.vocabulary_inv
        self.vocabulary_invmap = self.model.vocabulary_invmap
        self.cnn_model = self.model.cnn_model
        self.labels = self.model.labels
        self.classify = self.model.classify
        self.stopword_dict = self.model.stopword_dict

    def rm_stopword(self, text):
        text_list = text.split(' ')
        rm_result = [word for word in text_list if word not in self.stopword_dict and word != '']
        return ' '.join(rm_result)

    def cNNpredict(self, input):
        # 分词
        res = dp.content_to_list(input)  #分词预处理
        sentence = ' '.join(res)
        sentence1 = self.rm_stopword(sentence)

        # 取前三个类别及其概率
        s = self.cNNClassify_seg(sentence1)
        return s

    def cNNClassify_seg(self, input_seg):
        # 分词
        sentence = input_seg
        # 判断文本类别，返回文本在各类别上的概率值
        scores = predict_longText.predict(sentence, 300, self.vocabulary_invmap, self.cnn_model, self.labels)
        score = list(scores[0][0])#每一个类别的得分
        sort_scores = sorted(score, reverse=True)#得分从大到小排序
        tmp_str = str(score.index(sort_scores[0]))
        

        value_sum = 0.0
        value_sum += sort_scores[0] + sort_scores[1]
        s = self.classify[str(score.index(sort_scores[0]))]+':'+str(sort_scores[0] / value_sum)+' '+ \
                self.classify[str(score.index(sort_scores[1]))]+':' + str(sort_scores[1] / value_sum) 

        '''
        value_sum = 0.0
        value_sum += sort_scores[0] + sort_scores[1] + sort_scores[2]
        s = self.classify[str(score.index(sort_scores[0]))] + ':' + str(sort_scores[0] / value_sum) + ';' + \
            self.classify[
                str(score.index(sort_scores[1]))] + ':' + str(sort_scores[1] / value_sum) + ';' + self.classify[
                str(score.index(sort_scores[2]))] + ':' + str(sort_scores[2] / value_sum)
        '''

        s_all = ''
        len_all = len(sort_scores)
        sort_scores1 = sort_scores[:]
        score_min = sort_scores1[-1]
        value_sum1 = 0.0
        for i in range(len_all):
            sort_scores1[i] += math.fabs(score_min)
            value_sum1 += sort_scores1[i]
        print value_sum1
        for i in range(len_all):
            s_all += self.classify[str(score.index(sort_scores[i]))] + ':' + str(sort_scores1[i] / value_sum1) + ';'
        s_all = s_all[:-1]

        # 返回概率值最高的3个类别及对应的得分
        print s
        return s

if __name__ == '__main__':
    cc = CNNClassify()
    cc.cNNpredict('羽绒棉马甲女秋冬轻薄短款内胆  领【20】卷，卷后=￥29')

