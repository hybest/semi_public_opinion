#!/bin/sh

rm -fr  semi_train.txt

ls -l semi_train_*.txt | awk '{print $9}' | xargs -i -t cat {} >> ./semi_sample.txt
ls -l semi_train_*.txt | awk '{print $9}' | xargs -i -t rm {} -r

awk  -F ' ' '{ if(NF > 2) print $0 }' semi_sample.txt > semi_train.txt
rm -fr semi_sample.txt

