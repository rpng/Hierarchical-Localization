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

outputs = Path("outputs/sfm3/")
sfm_pairs = outputs / "pairs-exhaustive.txt"
sfm_dir = outputs / "sfm_superpoint+lightglue"

retrieval_conf = extract_features.confs["netvlad_rpng_half"]
feature_conf = extract_features.confs["superpoint_rpng4"]
matcher_conf = match_features.confs["superpoint+lightglue"]


# global matching
retrieval_path = extract_features.main(retrieval_conf, images, outputs)
references = [str(p.relative_to(images)) for p in (images).iterdir()]
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
