from pathlib import Path
from pprint import pformat
import argparse

from hloc import extract_features, match_features
from hloc import pairs_from_covisibility, pairs_from_retrieval
from hloc import colmap_from_nvm, triangulation, localize_sfm


parser = argparse.ArgumentParser()
parser.add_argument(
    "--dataset",
    type=Path,
    help="Path to the dataset, default: %(default)s",
)
parser.add_argument(
    "--outputs",
    type=Path,
    help="Path to the output directory, default: %(default)s",
)
parser.add_argument(
    "--num_covis",
    type=int,
    default=20,
    help="Number of image pairs for SfM, default: %(default)s",
)
args = parser.parse_args()

# Setup the paths
images = args.dataset

outputs = args.outputs  # where everything will be saved
sift_sfm = outputs / "sfm_sift"  # from which we extract the reference poses
reference_sfm = outputs / "sfm_superpoint+superglue"  # the SfM model we will build
sfm_pairs = (
    outputs / f"pairs-db-covis{args.num_covis}.txt"
)  # top-k most covisible in SIFT model

# list the standard configurations available
print(f"Configs for feature extractors:\n{pformat(extract_features.confs)}")
print(f"Configs for feature matchers:\n{pformat(match_features.confs)}")

# pick one of the configurations for extraction and matching
retrieval_conf = extract_features.confs["netvlad_rpng_half"]
feature_conf = extract_features.confs["superpoint_rpng3"]
matcher_conf = match_features.confs["superpoint+lightglue"]

features = extract_features.main(feature_conf, images, outputs)

pairs_from_covisibility.main(sift_sfm, sfm_pairs, num_matched=args.num_covis)
sfm_matches = match_features.main(
    matcher_conf, sfm_pairs, feature_conf["output"], outputs
)

triangulation.main(reference_sfm, sift_sfm, images, sfm_pairs, features, sfm_matches)
