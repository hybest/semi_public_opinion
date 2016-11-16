
#python get_cont_fromdb.py 20161006 20161106

#python cut_words_v4.py all_cont.txt

python gen_sample_v4.py chat_words.txt 

./semi_merge.sh

python split_sample.py semi_train.txt

python semi_superised_lp_v3.py

./get_cluster_data.sh 

python gen_sample_v3.py cluster_keywords.txt 

./merge.sh

./split.py train.txt

python hierarchy_cluster_v4.py 

./sort_rst.sh

./tj.sh


