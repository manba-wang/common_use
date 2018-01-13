#! /usr/bin/env python

import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers
from text_cnn import TextCNN

# Parameters
# ==================================================

# Model Hyperparameters
tf.flags.DEFINE_integer("embedding_dim", 100, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "3,4,5", "Comma-separated filter sizes (default: '3,4,5')")
tf.flags.DEFINE_integer("num_filters", 128, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.001, "L2 regularizaion lambda (default: 0.0)")

# Training parameters
tf.flags.DEFINE_integer("batch_size", 128, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("dev_batch_size", 1000, "Batch Size (default: 1000)")
tf.flags.DEFINE_integer("num_epochs", 100, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 100, "Evaluate model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 100, "Save model after this many steps (default: 100)")
# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

FLAGS = tf.flags.FLAGS
FLAGS.batch_size
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")

# Data Preparatopn
# ==================================================

# Load data
print("Loading data...")
x, y, vocabulary, vocabulary_inv = data_helpers.load_data()

# # Randomly shuffle data
# np.random.seed(10)
# shuffle_indices = np.random.permutation(np.arange(len(y)))
# x_shuffled = x[shuffle_indices]
# y_shuffled = y[shuffle_indices]
#
# percent_dev = 10
# dev_idx = -1*len(y_shuffled)//percent_dev
# # Split train/test set
# # TODO: This is very crude, should use cross-validation
# x_train, x_dev = x_shuffled[:dev_idx], x_shuffled[dev_idx:]
# y_train, y_dev = y_shuffled[:dev_idx], y_shuffled[dev_idx:]

# print("Vocabulary Size: {:d}".format(len(vocabulary)))
# print("Train/Dev split: {:d}/{:d}".format(len(y_train), len(y_dev)))
# build word vector matrix W
from gensim.models import Word2Vec
import random
print 'begin load word2vec model'
model = Word2Vec.load('wvm170825.model')
print 'finish load word2vec model'
# W = [model[v.decode('utf-8')]for v in vocabulary_inv]
W = []
outvoclabulary=open('dict/vocabulary_weibo_300.txt','w')

for v in vocabulary_inv:
    outvoclabulary.write(str(v)+'\n')
    try:
        W.append(np.float32(model[v]))
    except Exception, ex:
        l = []
        for i in range(FLAGS.embedding_dim):
            l.append(random.uniform(1, -1))
        W.append(np.float32(np.array(l)))
W = np.array(W)

print 'Done!'
