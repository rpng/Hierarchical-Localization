import numpy as np


def read_transform_data(filename):
    with open(filename, "r") as file:
        for line in file:
            if not line.startswith("#"):
                parts = line.split()
                # Hamilton
                q_CtoV = np.array([float(parts[i]) for i in range(0, 4)])
                p_CinV = np.array([float(parts[i]) for i in range(4, 7)])
                s_C2V = float(parts[7])
                break

    return np.array(q_CtoV), np.array(p_CinV), np.array(s_C2V)


if __name__ == "__main__":
    filename = "/home/yuxiang/workspace/Hierarchical-Localization/outputs/sfm/sfm_superpoint+superglue/transform_N2G.txt"  # Replace with your file name
    q_CtoV, p_CinV, s_C2V = read_transform_data(filename)
    print("q_CtoV:", q_CtoV)
    print("p_CinV:", p_CinV)
    print("s_C2V:", s_C2V)
    print()
