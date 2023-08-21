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
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--sfm_imgs", type=Path)
parser.add_argument("--sfm_model", type=Path)
parser.add_argument("--sfm_outputs", type=Path)
parser.add_argument("--query_imgs", type=Path)
parser.add_argument("--query_list", type=Path)
parser.add_argument("--query_outputs", type=Path)
parser.add_argument("--topn", type=int, default=5)
parser.add_argument("--global_feat", type=str)
parser.add_argument("--local_feat", type=str)
parser.add_argument("--match_method", type=str)
parser.add_argument("--result_name", type=str, default="result.txt")
args = parser.parse_args()

images = args.sfm_imgs
sfm_outputs = args.sfm_outputs
query_outputs = args.query_outputs
sfm_dir = args.sfm_model
loc_pairs = query_outputs / Path(
    "pairs-query-netvlad" + str(args.topn) + ".txt"
)  # top n retrieved by NetVLAD

results = query_outputs / args.result_name  # the result file

retrieval_conf = extract_features.confs[args.global_feat]
feature_conf = extract_features.confs[args.local_feat]
matcher_conf = match_features.confs[args.match_method]

# global feature extraction for
retrieval_path = extract_features.main(retrieval_conf, images, sfm_outputs)

# local feature extraction?-> this actually do nothing
feature_path = extract_features.main(feature_conf, images, sfm_outputs)

# query global matching
query = args.query_imgs
global_descriptors = extract_features.main(retrieval_conf, query, query_outputs)
pairs_from_retrieval.main(
    global_descriptors, loc_pairs, num_matched=args.topn, db_descriptors=retrieval_path
)

# query local matching
ffile = extract_features.main(feature_conf, query, query_outputs)
mfile = match_features.main(
    matcher_conf,
    loc_pairs,
    feature_conf["output"],
    query_outputs,
    features_ref=feature_path,
)

# localize query images in map
query_list = args.query_list
localize_sfm.main(sfm_dir, query_list, loc_pairs, ffile, mfile, results)
