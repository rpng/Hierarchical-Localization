from hloc.localize_sfm import QueryLocalizer, pose_from_cluster
import pycolmap
from pathlib import Path
from hloc import extract_features, match_features, reconstruction, visualization, pairs_from_retrieval, pairs_from_exhaustive, localize_sfm
images = Path('/home/tim/datasets/rpng_table/table_01_map/rgb-25')

outputs = Path('outputs/sfm/')
output_dir = Path('outputs/query/')
sfm_pairs = outputs / 'pairs-netvlad.txt'
sfm_dir = outputs / 'sfm_superpoint+superglue'
loc_pairs = outputs / 'pairs-query-netvlad20.txt'  # top 20 retrieved by NetVLAD

results = outputs / 'hloc_superpoint+superglue_netvlad20.txt'  # the result file

retrieval_conf = extract_features.confs['netvlad_rpng']
feature_conf = extract_features.confs['superpoint_rpng']
matcher_conf = match_features.confs['superglue']

# global matching
retrieval_path = extract_features.main(retrieval_conf, images, outputs)
pairs_from_retrieval.main(retrieval_path, sfm_pairs, num_matched=5)

# local matching
feature_path = extract_features.main(feature_conf, images, outputs)
match_path = match_features.main(
    matcher_conf, sfm_pairs, feature_conf['output'], outputs)

# build a model
model = reconstruction.main(
    sfm_dir, images, sfm_pairs, feature_path, match_path, camera_mode=pycolmap.CameraMode().OPENCV)

# # query global matching
# query = Path('/home/tim/datasets/rpng_table/table_01_imgs')
# global_descriptors = extract_features.main(retrieval_conf, query, output_dir)
# pairs_from_retrieval.main(global_descriptors, loc_pairs,
#                           num_matched=5, db_descriptors=retrieval_path)


# # Extract, match, amd localize.
# ffile = extract_features.main(feature_conf, query, output_dir)
# mfile = match_features.main(
#     matcher_conf, loc_pairs, feature_conf['output'], output_dir, features_ref=feature_path)

# query_list = Path("/home/tim/workspace/Hierarchical-Localization/output.txt")
# localize_sfm.main(
#     sfm_dir, query_list, loc_pairs, ffile, mfile, results, covisibility_clustering=False)
