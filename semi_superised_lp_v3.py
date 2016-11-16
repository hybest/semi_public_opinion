#coding=utf-8

import matplotlib.pyplot as plt
from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file
# from sklearn.semi_supervised import LabelPropagation
from sklearn.semi_supervised import label_propagation
# from sklearn.metrics import confusion_matrix, classification_report
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
print "load stopwords: %d" % len(doc_idx_mapping)

labeled_file = "labeled_train.txt"
tfidf_matrix, y_train = load_svmlight_file(labeled_file)
print tfidf_matrix.shape[0]
labeled_matrix = tfidf_matrix[:, 0:-1]
# print labeled_matrix[0]
train_array = labeled_matrix.toarray()
# print train_array[0]
#get docid
doc_matrix = tfidf_matrix[:, -1] #得到最后一列
doc_array = doc_matrix.toarray()
print int(doc_array[0])

unlabeled_file = "unlabeled_train.txt"
X_unlabeled_matrix, y_test = load_svmlight_file(unlabeled_file)
print X_unlabeled_matrix.shape[0]
unlabeled_matrix = X_unlabeled_matrix[:, 0:-1]
# print unlabeled_matrix[0]
unlabeled_array = unlabeled_matrix.toarray()
# print unlabeled_array[0]
#get docid
unlabeled_doc_matrix = X_unlabeled_matrix[:, -1] #得到最后一列
unlabeled_doc_array = unlabeled_doc_matrix.toarray()
print int(unlabeled_doc_array[0])

#exit()

# Learn with LabelPropagation
# label_prop_model = LabelPropagation(kernel='knn',n_neighbors=20, alpha=1, max_iter=2000)
# label_prop_model.fit(train_array, y_train)
# y_pred = label_prop_model.predict(unlabeled_array)



# Learn with LabelSpreading
lp_model = label_propagation.LabelSpreading( gamma=700 , max_iter=2000 )
lp_model.fit(train_array, y_train)
y_pred = lp_model.predict(unlabeled_array)

print y_pred
print ('predicting, classification error=%f' % (sum( int(y_pred[i]) != y_test[i] for i in range(len(unlabeled_array))) / float(len(unlabeled_array)) ) )

fd = open('positive_docid.txt','w')
cnt = 0
for i in range(len(unlabeled_array)):
    if y_pred[i] == 1:
        cnt += 1
        docid = int(unlabeled_doc_array[i])
        #print docid
        fd.write(str(docid) + "\n")
print("positive sample number: %d" %cnt)
fd.close()
