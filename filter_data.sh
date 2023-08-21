#!/usr/bin/env bash
clear

# bag
bagnames=(
"table_01"
"table_02"
"table_03"
"table_04"
"table_05"
"table_06"
"table_07"
"table_08"
)

result_path="Global_DS_Local_DS_200_Match_LG_top_5"
output_result_path="/home/yuxiang/results/hloc/$result_path"

# Loop through all datasets
for i in "${!bagnames[@]}"; do
    echo "${bagnames[i]}";
      
    python3 remove_badtime.py \
    /home/yuxiang/results/hloc_results/$result_path/${bagnames[i]}/bad.txt \
    /home/yuxiang/results/hloc_results/$result_path/${bagnames[i]}/ov_${bagnames[i]}.txt \
    /home/yuxiang/results/hloc_results/$result_path/${bagnames[i]}/ov_${bagnames[i]}_p.txt 

    python3 remove_badtime.py \
    /home/yuxiang/results/hloc_results/$result_path/${bagnames[i]}/bad.txt \
    /home/yuxiang/results/hloc_results/$result_path/${bagnames[i]}/vl_${bagnames[i]}.txt \
    $output_result_path/${bagnames[i]}/00_estimate.txt 

    echo "";
done
