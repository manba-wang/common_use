#!/data0/home/junbao/anaconda2/bin/python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from CNNClassifyService import CNNClassifyService
import jieba
import os
import predict_longText
import ModelLoader_longText
import json
import math
import time
import datetime
from proprecess.corpusPreprocess import  weiboPreprocess

MY_WORK_SPACE = os.environ['MY_WORK_SPACE']
sys.path.append(MY_WORK_SPACE)
from keywords.tokenizer_handler import *

from thrift.transport import TSocket
from thrift.transport import TTransport
#from thrift.protocol import TCompactProtocol
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.server import TProcessPoolServer


ISOTIMEFORMAT='%Y-%m-%d %X'

class CNNClassify:
    #def __init__(self, vocabulary_inv, vocabulary_invmap,cnn_model, labels, classify, bayes_model,hot_top_map, stopword_dict,tagword_dict,cateIdName):

    def __init__(self, vocabulary_inv, vocabulary_invmap, cnn_model, labels, classify,stopword_dict,word_cls_map):
        self.vocabulary_inv = vocabulary_inv
        self.vocabulary_invmap = vocabulary_invmap
        self.cnn_model = cnn_model
        self.labels = labels
        self.classify = classify
        #self.bayes_model=bayes_model
        #self.hot_top_map=hot_top_map
        self.stopword_dict = stopword_dict
        self.word_cls_map = word_cls_map
        self.th = TokenizerHandler()
        #self.tagword_dict = tagword_dict
        #self.cateIdName = cateIdName

    """
    对文本进行分词
    输入文本内容，输出分词后用空格隔开的文本
    """
    def jieba_seg_s(self, text):
        seg_result = ' '.join(jieba.cut(text))
        return seg_result

    """
        去除停用词
        输入文本内容，输出分词后用空格隔开的文本
    """
    def rm_stopword(self, text):
        text_list = text.split(' ')
        rm_result = [word for word in text_list if word not in self.stopword_dict and word != '']
        return ' '.join(rm_result)

    """
    对输入的内容分类
    输出前三个类别及概率，格式为K:V
    """
    def cNNClassify(self, input):
        #首先进行微博预处理
        input = weiboPreprocess(input)
        # 分词
        #sentence = self.jieba_seg_s(input) #jieba
        sentence = self.th.split(input,tag_human_readable=False)
        res = [x['word'] for x in sentence] 
        sentence = ' '.join(res)
        sentence1 = self.rm_stopword(sentence)

        # 取前三个类别及其概率
        s = self.cNNClassify_seg(sentence1)
        return s


    def cNNClassify_seg(self, input_seg):
        # 分词
        sentence = input_seg
        # 判断文本类别，返回文本在各类别上的概率值
        scores = predict_longText.predict(sentence, 500, self.vocabulary_invmap, self.cnn_model, self.labels)
        score = list(scores[0][0])

        sort_scores = sorted(score, reverse=True)
        tmp_str = str(score.index(sort_scores[0]))

        # t = str(score.index(sort_scores[0]))
        #print 'sort_scores',sort_scores
        
        value_sum = 0.0
        value_sum += sort_scores[0] + sort_scores[1] + sort_scores[2]
        s = self.classify[str(score.index(sort_scores[0]))] + ':' + str(sort_scores[0] / value_sum) + ';' + self.classify[
                str(score.index(sort_scores[1]))] + ':' + str(sort_scores[1] / value_sum) + ';' + self.classify[
                str(score.index(sort_scores[2]))] + ':' + str(sort_scores[2] / value_sum)
        
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
        
        #rule_class = ''
        # for word in self.word_cls_map:
        #     if word in sentence:
        #         rule_class = self.word_cls_map[word]
        #         s = rule_class

        #返回概率值最高的3个类别及对应的得分
        return s

    def bayesClassify(self, input):
        # 分词
        sentence = self.jieba_seg_s(input)
        result=self.bayesClassify_seg(sentence)

        return result

    def bayesClassify_seg(self, input_seg):
        # 分词
        sentence = input_seg
        segarr=sentence.split(' ')
        catevalue={}

        for tmpword in segarr:
            try:
                tmpinfor=self.bayes_model[tmpword]
                #print tmpinfor
                tcatescorearr=tmpinfor.split(';')
                for tmpcatescore in tcatescorearr:
                    tmparr=tmpcatescore.split('\001')
                    tcate=tmparr[0]
                    tscore=float(tmparr[1])
                    print tcate

                    if tcate in catevalue:
                        catevalue[tcate]+=tscore
		        #print tcate
			#print tscore
                    else:
                        catevalue[tcate]=tscore
            except Exception, ex:
                pass

	    #print len(catevalue)
        sorted_catevalue=sorted(catevalue.items(), key= lambda x:x[1], reverse=True)
        result = ''
        #print len(sorted_catevalue)

        for i in range(len(sorted_catevalue)):
             result += sorted_catevalue[i][0]+':'+str(sorted_catevalue[i][1])+';'
             if i==3:
                 break;
        #print input_seg
        #print result
        return result[:-1]

    def classify_combine(self, input):

        # 分词
        # print datetime.datetime.now().isoformat()+'cnn_start'

        sentence = self.jieba_seg_s(input)
        # print datetime.datetime.now().isoformat() + 'seg_word'
        sentence1 = self.rm_stopword(sentence)

        # 判断文本类别，返回文本在各类别上的概率值
        scores = predict_longText.predict(sentence1, 500, self.vocabulary_invmap, self.cnn_model, self.labels)
        score = list(scores[0][0])
        sort_scores = sorted(score, reverse=True)

        result_list=[]

        # 取第一个类别
        s_top = self.cateIdName[str(self.classify[str(score.index(sort_scores[0]))])]
        if s_top in ['娱乐明星','音乐','电影','电视剧','综艺','dj']:
            s_top='娱乐'
        if s_top =='社会时政':
            s_top='时事'

        result=s_top
        result_list.append(s_top)

        list_sen=sentence1.split(' ')
        iword=0
        pre_word=''
        pre_pre_word=''

        for wordt in list_sen:

            if str(wordt) in self.tagword_dict and len(wordt)>1:
                tag_cate=self.tagword_dict[str(wordt)]
                if tag_cate in ['娱乐明星','音乐','电影','电视剧','综艺','dj']:
                    tag_cate='娱乐'

                if tag_cate==s_top or tag_cate=='其他' or tag_cate=='IT技术':
                    if wordt not in result_list:
                        result+=','
                        result+=str(wordt)
                        result_list.append(wordt)
            if iword>=1:
                dou_word=str(pre_word)+str(wordt)
                if str(dou_word) in self.tagword_dict and len(dou_word)>1:
                    tag_cate=self.tagword_dict[str(dou_word)]
                    if tag_cate in ['娱乐明星', '电影', '电视剧', '综艺', 'dj']:
                        tag_cate = '娱乐'
                    if tag_cate==s_top or tag_cate=='其他' or tag_cate=='IT技术':
                        if dou_word not in result_list:
                            result+=','
                            result+=str(dou_word)
                            result_list.append(dou_word)
            if iword>=2:
                thi_word=str(pre_pre_word)+str(pre_word)+str(wordt)
                if str(thi_word) in self.tagword_dict and len(thi_word)>1:
                    tag_cate = self.tagword_dict[str(thi_word)]
                    if tag_cate in ['娱乐明星', '电影', '电视剧', '综艺', 'dj']:
                        tag_cate = '娱乐'
                    if tag_cate == s_top or tag_cate == '其他' or tag_cate == 'IT技术':
                        if thi_word not in result_list:
                            result+=','
                            result+=str(thi_word)
                            result_list.append(thi_word)

            pre_pre_word=pre_word
            pre_word=wordt
            iword+=1

        return result

    def classify_hot_top(self, input):
        result='hot_top'
        return result

if __name__ == '__main__':
    print 'star main...\n'

    model = ModelLoader_longText.ModelLoader()

    print 'all init finished!\n'

    handler = CNNClassify(model.vocabulary_inv, model.vocabulary_invmap,model.cnn_model, model.labels, model.classify,model.stopword_dict,model.word_cls_map) #原始全部的
    #handler = CNNClassify(model.vocabulary_inv, model.vocabulary_invmap, model.cnn_model, model.labels,model.stopword_dict)
    print 'CNNClassify init finished!\n'
    processor = CNNClassifyService.Processor(handler)

    transport = TSocket.TServerSocket(port=10012)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    server.serve()

    print 'server start!\n'
