from hloc.localize_sfm import QueryLocalizer, pose_from_cluster
import pycolmap
from pathlib import Path
from hloc import (
    extract_features,
    match_features,
    reconstruction,
    visualization,
    pairs_from_retrieval,
    pairs_from_exhaustive,
    localize_sfm,
)

images = Path("/home/yuxiang/datasets/rpng_table/table_01_map/rgb-222")
outputs = Path("outputs/sfm/")
output_dir = Path("outputs/query4_t3/")
sfm_dir = outputs / "sfm_superpoint+superglue"
loc_pairs = outputs / "pairs-query-netvlad20.txt"  # top 20 retrieved by NetVLAD

results = output_dir / "hloc_superpoint+superglue_netvlad20.txt"  # the result file

retrieval_conf = extract_features.confs["netvlad_rpng"]
feature_conf = extract_features.confs["superpoint_rpng"]
matcher_conf = match_features.confs["superpoint+lightglue"]

# global matching
retrieval_path = extract_features.main(retrieval_conf, images, outputs)

# local matching
feature_path = extract_features.main(feature_conf, images, outputs)

# query global matching
query = Path("/home/yuxiang/datasets/rpng_table/table_02_imgs")
global_descriptors = extract_features.main(retrieval_conf, query, output_dir)
pairs_from_retrieval.main(
    global_descriptors, loc_pairs, num_matched=20, db_descriptors=retrieval_path
)


# query local matching
ffile = extract_features.main(feature_conf, query, output_dir)
mfile = match_features.main(
    matcher_conf,
    loc_pairs,
    feature_conf["output"],
    output_dir,
    features_ref=feature_path,
)

# localize query images in map
query_list = Path("/home/yuxiang/workspace/Hierarchical-Localization/output2.txt")
localize_sfm.main(sfm_dir, query_list, loc_pairs, ffile, mfile, results)
