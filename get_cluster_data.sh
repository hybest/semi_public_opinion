
awk -F '\t' 'NR==FNR{a[$1]=$0;next}NR>FNR{if($1 in a) print $0 }' positive_docid.txt chat_words.txt > cluster_words.txt

awk -F '\t' 'NR==FNR{a[$1]=$0;next}NR>FNR{if($1 in a) print $0 }' positive_docid.txt chat_keywords.txt > cluster_keywords.txt

