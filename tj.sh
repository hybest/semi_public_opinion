
awk -F ' ' '{ number[$1]++}END{for(i in number) print i, number[i]}' OFS="\t"  hac_all_rst_final.txt | sort -k2nr
