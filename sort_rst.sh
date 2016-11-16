
cat hac_result.txt hac_pre_rst.txt > hac_all_rst.txt

cat hac_result.txt | sort -k1n > hac_result_final.txt

cat hac_all_rst.txt | sort -k1n > hac_all_rst_final.txt

