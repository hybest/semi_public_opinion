#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import random
import sys


if len(sys.argv) <= 1:
  print "need to set input file"
  sys.exit(-1)

all_lines = []
for line in open(sys.argv[1], "r"):
  all_lines.append(line)
#random.shuffle(all_lines)

if len(sys.argv) > 2:
  test_rate = float(sys.argv[2])
else:
  test_rate = 0.2


test_size = int(len(all_lines)*test_rate)
train_size = len(all_lines) - test_size 

if train_size > 0:
  fp = open("d_train.txt",  "w")
  for v in all_lines[:train_size]:
    fp.write(v)
  fp.close()

if test_size > 0:
  fp = open("d_test.txt", "w")
  for v in all_lines[-test_size:]:
    fp.write(v)
  fp.close()

