#coding=utf-8

import os
import sys
import time
import datetime
import pickle
from text_feature import TextFeature
from multiprocessing import Process, Pool, Queue

def BuildJob(q, fn, cs):
  f = TextFeature()
  cache = []
  cnt = 0

  while True:
    r = q.get(True)
    cnt += 1
    if cnt % 10000 == 0:
      print "build %s: %d" % (fn, cnt)

    if r is None:
      if len(cache) > 0:
        f.Build(cache)
        cache = []
      if fn == 'chat_text_f.dat':
	print "prune..."
        f.Prune(2, 2)
      pickle.dump(f, open(fn, "w"))
      print "feature build %s succ" % fn
      return
    else:
      cache.append(r)
      if len(cache) >= cs:
        f.Build(cache)
        cache = []


q_norm = Queue(10*10000)
jobs = []


p = Process(target = BuildJob, args = (q_norm, "chat_text_f.dat", 100))
jobs.append(p)
p.start()

# word_vec =[]
cnt = 0

for line in open(sys.argv[1], "r"):
#for line in open("test.txt", "r"):
  cnt += 1
  if cnt % 1000 == 0:
    time_str = datetime.datetime.now().isoformat()
    print "[%s]: %d" % (time_str, cnt)

  # parts = json.dumps(line.strip())
  # print parts

  words = ""
  kw_vec = line.strip().split(" ")
  q_norm.put(kw_vec)

  # print kw_vec
  words += " ".join(kw_vec)

q_norm.put(None)
for job in jobs:
  job.join()

print "dump text feature succ"
os._exit(-1)

