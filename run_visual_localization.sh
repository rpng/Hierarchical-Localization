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

#estimation mode
topn=(
  "5"
  "10"
  "20"
)

# Loop through all datasets
save_dir="/home/yuxiang/results/ov_nerf_results"
for i in "${!bagnames[@]}"; do
  for j in "${!topn[@]}"; do
    echo "**************************************************************************";
    echo "BASH: ${bagnames[i]} - top ${topn[j]} starts!";
    start_time="$(date -u +%s)"
      
    python3 localization.py \
    --sfm_imgs "/home/yuxiang/datasets/rpng_table/table_01_map/rgb-222" \
    --sfm_model "/home/yuxiang/datasets/rpng_table/table_01_map/sfm_superpoint+superglue" \
    --sfm_outputs "/home/yuxiang/datasets/rpng_table/table_01_map" \
    --query_imgs "/home/yuxiang/datasets/rpng_table/${bagnames[i]}_imgs" \
    --query_outputs "/home/yuxiang/results/hloc_results/${bagnames[i]}" \
    --topn "${topn[j]}" \
    --global_feat "netvlad_rpng_half" \
    --local_feat "superpoint_rpng3" \
    --match_method "superpoint+lightglue" \
    --query_list /home/yuxiang/workspace/Hierarchical-Localization/query_list/${bagnames[i]}_colmap_intrinsic.txt

    python3 result_vl_to_ov.py \
    --transform_path "/home/yuxiang/datasets/rpng_table/table_01_map/sfm_sift/transform_NtoG.txt" \
    --orig_result_path "/home/yuxiang/results/hloc_results/${bagnames[i]}/result.txt" \
    --vlresult_path  "/home/yuxiang/results/hloc_results/${bagnames[i]}/vl_${bagnames[i]}.txt" \
    --ovresult_path "/home/yuxiang/results/hloc_results/${bagnames[i]}/ov_${bagnames[i]}.txt"
    

    # print out the time elapsed
    end_time="$(date -u +%s)"
    elapsed="$(($end_time-$start_time))"
    echo "BASH: ${bagnames[i]} - top ${topn[j]} took $elapsed seconds";
    echo "**************************************************************************";    
    echo "";
  done
done
