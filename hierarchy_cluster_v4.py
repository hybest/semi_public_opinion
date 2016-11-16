#coding=utf-8

from sklearn.datasets import load_svmlight_file
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pickle
from text_feature import TextFeature
import datetime

text_fea    = pickle.load(open('chat_text_f.dat'))
vocab_mapping = dict((value,key) for key,value in text_fea.vocab_dict.iteritems())
#for k,v in vocab_mapping.items():
#    print "key:"+str(k)+",value:"+v

doc_idx_mapping = dict()
for line in open("doc_idx.txt", "r"):
  doc_idx = int(line.strip().split(' ')[0])
  docname = line.strip().split(' ')[1]
  doc_idx_mapping[doc_idx] = docname

train_file = "d_train.txt"
test_file = "d_test.txt"
tfidf_matrix, y_train = load_svmlight_file(train_file)
print tfidf_matrix.shape[0]
train_array = tfidf_matrix.toarray()

test_matrix, y_test = load_svmlight_file(test_file)
test_array = test_matrix.toarray()

#knn_graph = kneighbors_graph(train_array, 20, include_self=False)

linkage = 'average'
#linkage = 'complete'
print " will exec model..."
model = AgglomerativeClustering(affinity="cosine",linkage=linkage,
                                    n_clusters=200)

model.fit(train_array)
print "hac cluster result..."
print model.labels_

print "save model..."
from sklearn.externals import joblib
joblib.dump(model, 'hac_model.pkl')

fn = "hac_result.txt"
fp = open(fn,"w")

cnt = 0
sample_lists = []
for line in open(train_file, "r"):
  line_list = line.strip().split(" ")
  label = int(line_list[0])
  idx_list = line_list[1:-1]
  # print idx_list

  word_list = []
  words = ""
  for m in range(len(idx_list)):
      idx = idx_list[m].split(":")[0]
      word = vocab_mapping[int(idx)-1]
      # print word
      word_list.append(word)
  #print word_list
  words += " ".join(word_list)
  #print words
  sample_lists.append(word_list)
  fp.write(str(model.labels_[cnt]) +" " + str(label) +" " + doc_idx_mapping[label] + " " +words + "\n")
  cnt += 1

fp.close()
print len(sample_lists)

print "will predict..."
pre_clusters = model.fit_predict(test_array)
print pre_clusters
# dump_svmlight_file(test_matrix,pre_clusters,'hac_pre_rst.txt',zero_based=True,multilabel=False)

tr_name = "hac_pre_rst.txt"
ft = open(tr_name,"w")

cnt = 0
for line in open(test_file, "r"):
  line_list = line.strip().split(" ")
  label = int(line_list[0])
  idx_list = line_list[1:-1]
  # print idx_list

  word_list = []
  words = ""
  for m in range(len(idx_list)):
      idx = idx_list[m].split(":")[0]
      word = vocab_mapping[int(idx)-1]
      # print word
      word_list.append(word)
  #print word_list
  words += " ".join(word_list)
  #print words
  ft.write(str(pre_clusters[cnt]) +" " + str(label) +" " + doc_idx_mapping[label] + " " +words + "\n")
  cnt += 1
ft.close()

