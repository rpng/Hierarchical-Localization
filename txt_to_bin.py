from hloc.utils.read_write_model import (
    read_cameras_text,
    read_images_text,
    read_points3D_text,
    write_cameras_binary,
    write_images_binary,
    write_points3D_binary,
)

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=Path, required=True)
args = parser.parse_args().__dict__

cameras = read_cameras_text(args["path"] / "cameras.txt")
images = read_images_text(args["path"] / "images.txt")
points3D = read_points3D_text(args["path"] / "points3D.txt")
write_cameras_binary(cameras, args["path"] / "cameras.bin")
write_images_binary(images, args["path"] / "images.bin")
write_points3D_binary(points3D, args["path"] / "points3D.bin")
