#!/bin/sh

rm -fr sample.txt train.txt

ls -l cluster_train_*.txt | awk '{print $9}' | xargs -i -t cat {} >> ./sample.txt
ls -l cluster_train_*.txt | awk '{print $9}' | xargs -i -t rm {} -r

awk  -F ' ' '{ if(NF > 2) print $0 }' sample.txt > train.txt
rm -fr sample.txt

