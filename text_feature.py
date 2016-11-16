#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import json

'''
input: [ ['a', 'b', 'c'], ['a', 'a', 'c']]
ouput:[[1, 1, 1], [2, 0, 1]]

meta:
need_build: False
vocab: {'a':0, 'b': 1, 'c': 2}
vocab_list: []
df  :  {'a': 2, 'b': 1, 'c': 2}
total_tf: 6
total_df: 2
'''

def Test():
  x = [['a', 'a', 'b', 'c'], ['a', 'a', 'a'], ['c', 'b', 'b', 'b']]
  m = TextFeature()
  r = m.Trans(x)
  print "after trans:"
  print json.dumps(r, ensure_ascii=False, indent=2,encoding='utf8')
  #m.Dump()

class TextFeature(object):
  def __init__(self):
    self.total_tf = 0
    self.total_df = 0
    self.total_wc = 0
    self.vocab_dict = dict()
    self.vocab_list = []
    self.df = dict()
    self.tf = dict()

  def Dump(self):
    print "vocab_dict:"
    print json.dumps(self.vocab_dict, ensure_ascii=False, indent=2,encoding='utf8')
    print "vocab_list:"
    print json.dumps(self.vocab_list, ensure_ascii=False, indent=2,encoding='utf8')
    print "df:"
    print json.dumps(self.df, ensure_ascii=False, indent=2,encoding='utf8')
    print "tf:"
    print json.dumps(self.tf, ensure_ascii=False, indent=2,encoding='utf8')
    print "total_tf: %d, total_df: %d, total_wc: %d" % (self.total_tf, self.total_df, self.total_wc)

  def Build(self, corps):
    self.total_df += len(corps)
    for corp in corps:
      self.total_tf += len(corp)
      doc_set = dict()
      for term in corp:
        doc_set[term] = 1
        if not self.vocab_dict.has_key(term):
          self.vocab_dict[term] = len(self.vocab_list)
          self.vocab_list.append(term)
          self.df[term] = 0
          self.tf[term] = 0
        self.tf[term] += 1

      for term in doc_set.keys():
        self.df[term] += 1
    self.total_wc = len(self.vocab_list)

  def Prune(self, min_df, min_tf):
    new_vocab_list = []
    new_vocab_dict = dict()
    for v in self.vocab_list:
      if self.df[v] < min_df or self.tf[v] < min_tf:
        continue
      new_vocab_dict[v] = len(new_vocab_list)
      new_vocab_list.append(v)
    self.vocab_dict = new_vocab_dict
    self.vocab_list = new_vocab_list
    self.total_wc = len(self.vocab_list)

  def Trans(self, corps):
    rvs = []
    for corp in corps:
      if not type(corp) is list:
        raise Exception('exeption', 'corp type is list')

      rv = [0.0]*self.total_wc
      freq = dict()
      for term in corp:
        freq[term] = freq.get(term, 0) + 1

      #print "============== doc:%s" % (str(corp))
      dl = float(len(corp))
      for (k, v) in freq.items():
        if not self.vocab_dict.has_key(k):
          continue
        idx = self.vocab_dict[k]
        word_tf = float(v)
        word_df = float(self.df[k])
        total_df = float(self.total_df + 1)
        tf_idf = (word_tf/dl)*math.log(total_df/word_df)
        rv[idx] = tf_idf
      rvs.append(rv)
    return rvs

  def GetDf(self):
    return self.df

  def GetVocab(self):
    return self.vocab_dict

