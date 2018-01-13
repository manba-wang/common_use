python2.7

data_helper加载训练集、设置截断长度
train_weibo_new设置训练参数，开始训练（训练采用gensim预训练的词向量的加载）

built_vocabulary_weibo构建词典，用于预测，

ModelLoader_longText加载模型，包括词典、类别映射、词向量、cnn模型
predict_longText用于预测
cnn_predict输出预测值

