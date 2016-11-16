#coding=utf-8

from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file
from sklearn.cluster import AgglomerativeClustering
from sklearn.externals import joblib


hac_model = joblib.load('hac_result.pkl')

tfidf_matrix, y_train = load_svmlight_file("./d_train.txt")

dump_svmlight_file(tfidf_matrix,hac_model.labels_,'hac_train_rst.txt',zero_based=True,multilabel=False)

