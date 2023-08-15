from hloc.localize_sfm import QueryLocalizer, pose_from_cluster
import pycolmap
from pathlib import Path
import os
from hloc import (
    extract_features,
    match_features,
    reconstruction,
    visualization,
    pairs_from_retrieval,
    pairs_from_exhaustive,
)

images = Path("/home/yuxiang/datasets/rpng_table/table_01_map/rgb-222")

outputs = Path("outputs/sfm/")
sfm_pairs = outputs / "pairs-netvlad.txt"
sfm_dir = outputs / "sfm_superpoint+superglue"
loc_pairs = outputs / "pairs-query-netvlad20.txt"  # top 20 retrieved by NetVLAD

results = outputs / "hloc_superpoint+superglue_netvlad20.txt"  # the result file

retrieval_conf = extract_features.confs["netvlad_rpng"]
feature_conf = extract_features.confs["superpoint_rpng"]
matcher_conf = match_features.confs["superglue"]


# global matching
retrieval_path = extract_features.main(retrieval_conf, images, outputs)

references = [str(p.relative_to(images)) for p in (images).iterdir()]
print(references)
pairs_from_exhaustive.main(sfm_pairs, image_list=references)

# local matching
feature_path = extract_features.main(feature_conf, images, outputs)
match_path = match_features.main(
    matcher_conf, sfm_pairs, feature_conf["output"], outputs
)

# build a model
image_options = pycolmap.ImageReaderOptions()
image_options.camera_model = "OPENCV"
model = reconstruction.main(
    sfm_dir,
    images,
    sfm_pairs,
    feature_path,
    match_path,
    camera_mode=pycolmap.CameraMode.SINGLE,
    image_options=image_options,
)
