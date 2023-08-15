from hloc.utils.read_write_model import read_cameras_binary

camera = read_cameras_binary(
    "/home/tim/workspace/Hierarchical-Localization/outputs/sfm/sfm_superpoint+superglue/cameras.bin")
print(camera)
