# Scripts Documents

## 1. Colmap Format transform

```shell
python3 bin_to_txt.py \
--path "/home/yuxiang/workspace/Hierarchical-Localization/outputs/sfm/sfm_superpoint+superglue"

python3 txt_to_bin.py \
--path "/home/yuxiang/workspace/Hierarchical-Localization/outputs/sfm/sfm_superpoint+superglue"

```

## 2. Triangulate a Model Given SfM Poses in bin

```shell
python3 retriangulate_model.py \
--dataset /home/yuxiang/datasets/rpng_table/table_01_map/rgb-222 \
--outputs /home/yuxiang/datasets/rpng_table/table_01_map
```

## 3. Generate Query List

This is where you change the camera intrinsic for the query images

```shell
python3 generate_query_list.py
```

## 4. Run localization

```shell
./run_visual_localization
```

## 4. Filter Bad Localization Result

This is only for evaluation, if doing tightly couple, we need to include all.

```shell
# 1. Get bad timestamp
# in ov_nerf loop-closure branch
rosrun ov_eval error_singlerun_v2 none /home/yuxiang/workspace/ov_nerf_ws/src/ov_nerf/ov_data/rpng_table/table_02.txt  /home/yuxiang/results/hloc_results/Global_DS_Local_DS_200_Match_LG/table_02/ov_table_02.txt /home/yuxiang/results/hloc_results/Global_DS_Local_DS_200_Match_LG/table_02/bad.txt

# 2. Remove bad timestamp and generate a new file
./filter_data.sh
```
