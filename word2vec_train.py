#!/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from gensim.models import word2vec
import logging 
import time
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

"""加载的数据为json格式，每一行是一个文件或者一段话分词之后的字符串,json.dumps之后的"""

class Word2vec_train():
    def __init__(self,num_features=200,min_word_count=3,context = 5,load_path=None,model_name=None):
        self.num_features = num_features  # 词向量维度
        self.min_word_count = min_word_count  # 最少单词数量
        self.context = context  # 文本窗口大小 
        self.model_name = model_name
        self.load_path = load_path
    
    def calcu_docs(self): 
        datas = open(self.load_path).readlines()
        return len(datas)

    def load_corpus(self):
        datas = open(self.load_path).readlines()
        for data in datas[:-1]:
            if data:
                data = json.loads(data)            
                yield data.split()

    def word2vec(self):
        print 'initializing model...'
        start = time.time()
        model = word2vec.Word2Vec(size=self.num_features, min_count=self.min_word_count,window=self.context)
        stop = time.time()
        print 'initializing model costs %s seconds...' % (stop - start)

        print 'building vocabulary...'
        start = time.time()
        model.build_vocab(self.load_corpus())
        stop = time.time()
        print 'building vocabulary costs %s seconds...' % (stop - start)

        print 'training...'
        start = time.time()
        total_examples = self.calcu_docs()
        model.train(self.load_corpus(),total_examples =total_examples,epochs=model.iter)
        stop = time.time()
        print 'training costs %s seconds...' % (stop - start)

        print 'saving model...'
        start = time.time()
        model.save(model_name)
        stop = time.time()
        print 'saving model costs %s seconds...' % (stop - start)

    def test(self,word,topn):
        model = word2vec.Word2Vec.load(model_name)
        similar_words = model.most_similar(positive=[word], topn=topn)
        for word, weight in similar_words:
            print word, weight

    def test2(self):
        model = word2vec.Word2Vec.load(model_name)
        all_words = model.vocab.items()
        print all_words

    def test3(self,list1,list2):
        model = word2vec.Word2Vec.load(model_name)
        sim = model.n_similarity(list1,list2)
        print sim

if __name__ == "__main__":
    path = 'corpus/souhu_all.json'
    model_name = 'model/souhu_all.model'
    wt = Word2vec_train(load_path = path,model_name=model_name,min_word_count=0)
    wt.word2vec()
    wt.test(u'自闭症',10)
    # wt.test3([u'华盛顿',u'北京'],[u'美国',u'中国'])

