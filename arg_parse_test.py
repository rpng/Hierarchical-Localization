import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--sfm_dir", type=Path, required=True)
parser.add_argument("--fuck", type=float, required=True)
args = parser.parse_args().__dict__

print(args)
print(args["fuck"] + 1)
