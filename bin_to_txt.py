from hloc.utils.read_write_model import (
    read_cameras_binary,
    read_images_binary,
    write_cameras_text,
    write_images_text,
)

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=Path, required=True)
args = parser.parse_args().__dict__

cameras = read_cameras_binary(args["path"] / "cameras.bin")
images = read_images_binary(args["path"] / "images.bin")
write_cameras_text(cameras, args["path"] / "cameras.txt")
write_images_text(images, args["path"] / "images.txt")
