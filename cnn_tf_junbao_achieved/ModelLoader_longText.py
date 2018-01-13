# coding=utf-8
import predict_longText

class ModelLoader:
    def __init__(self):
        # 定义服务器的模型目录
        self.CNNModle_path = "/data0/home/shixi_wangtao1/wangtao/advert/advert_cnn/"
        # 定义cnn模型
        self.cnn_path = self.CNNModle_path + "runs/1506050254/checkpoints/model-5100"

        #定义特定词与类别的映射
        #self.word_cls_path = self.CNNModle_path + "dict/word_cls_dict.txt"

        # 定义word2vec模型
        self.w2v_path = self.CNNModle_path + "wvm170825.model"

        # 定义标签映射
        self.cate_path = self.CNNModle_path + "dict/cate_ad.txt"

        # 定义词典路径
        self.vocabulary_inv_path = self.CNNModle_path + "dict/vocabulary_weibo_300.txt"

        # 定义停用词路径
        self.stopword_path = self.CNNModle_path + "dict/stopword.txt"

        # 定义所有领域标签集合
        #self.tagworddict_path = self.CNNModle_path + "dict/bigdata_tag_1216_all.txt"

        # 定义句子长度，固定值与训练模型的句子长度一致
        self.sequence_lenth = 300
        # 停用词典
        self.stopword_dict = {}
        stopword = open(self.stopword_path, 'r')
        for line4 in stopword:
            self.stopword_dict.setdefault(line4.strip(), '')
        print '加载停用词词典完成\n'

        # 加载类别信息,进行标签映射
        
        self.classify = {}
        #self.cateIdName = {}
        cate = open(self.cate_path, 'r')
        for line2 in cate:
            line2_list = line2.strip().split(' ')
            if(len(line2_list) >= 3):
                self.classify[line2_list[-1]] = line2_list[-3]    #存储cnn返回类别id 与 类别中文 的对应classify[0]='中文类别'
                #self.cateIdName[line2_list[3]] = line2_list[0]  #y_009 映射 动漫
        print '加载标签完成\n'

        '''
        self.word_cls_map = {}
        fin = open(self.word_cls_path,'r')
        for line in fin:
            line1 = line.strip().split('\t')
            if(len(line1) >= 2):
                self.word_cls_map[line1[0]] = line1[1]
        fin.close()
        print '加载特定词完成.\n'
        '''

        # 加载标签
        l = 2
        self.labels = []
        for j in range(l):
            self.labels.append(0)

        # 加载词表
        f = open(self.vocabulary_inv_path, 'r')
        self.vocabulary_invmap= {}
        self.vocabulary_inv = []
        inv_index = 0

        for line in f:
            self.vocabulary_inv.append(line.strip())
            self.vocabulary_invmap.setdefault(line.strip(), inv_index)
            inv_index += 1
        print len(self.vocabulary_invmap),inv_index
        print len(self.vocabulary_inv)
        print '加载词典完成\n'

        # 加载词向量矩阵
        self.W = predict_longText.load_wv_model(self.w2v_path, self.vocabulary_inv)
        print '加载词向量完成\n'

        # 加载cnn模型
        self.cnn_model = predict_longText.load_cnn(self.sequence_lenth, self.W, self.cnn_path, len(self.vocabulary_inv))
        print '加载CNN模型完成\n'

        '''
        #加载bayes模型
        self.bayes_model = {}
        fbayes = open(self.bayes_path,'r')
        for line1 in fbayes:
            line1_list=line1.strip().split('\t')
            self.bayes_model[line1_list[0]]=line1_list[1]
        print '加载bayes模型完成\n'

        #加载hot_top_map
        self.hot_top_map = {}
        fhot = open(self.hot_top_path, 'r')
        for line3 in fhot:
            line3_list = line3.strip().split('\t')
            self.hot_top_map[line3_list[0]] = line3_list[1]
        print '加载热门行业模型完成\n'

        #加载标签词典
        self.tagword_dict = {}
        ftag=open(self.tagworddict_path,'r')
        for line4 in ftag:
            line4_list = line4.strip().split('\t')
            if len(line4_list)<2:
                continue
            self.tagword_dict[line4_list[0]] = line4_list[1]
        print len(self.tagword_dict)
        print '加载标签词典完成\n'
        '''
