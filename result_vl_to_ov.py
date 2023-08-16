import numpy as np
from scipy.spatial.transform import Rotation as R
import argparse
from pathlib import Path


def parse_line(line):
    parts = line.split()
    timestamp_str = parts[0].split(".")[0]  # Extract the timestamp part before '.png'
    timestamp = float(
        timestamp_str[:10] + "." + timestamp_str[10:]
    )  # Format the timestamp
    rotation = np.array([float(parts[i]) for i in range(1, 5)])
    translation = np.array([float(parts[i]) for i in range(5, 8)]).reshape([3, 1])
    return {"timestamp": timestamp, "q_NtoC": rotation, "p_NinC": translation}


# hamiltonian quaternion convention
def qvec2rotmat(qvec):  # TODO: double check this
    return np.array(
        [
            [
                1 - 2 * qvec[2] ** 2 - 2 * qvec[3] ** 2,
                2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
                2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2],
            ],
            [
                2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
                1 - 2 * qvec[1] ** 2 - 2 * qvec[3] ** 2,
                2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1],
            ],
            [
                2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
                2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
                1 - 2 * qvec[1] ** 2 - 2 * qvec[2] ** 2,
            ],
        ]
    )


def rotmat2qvec(rotm):  # TODO: double check this
    return R.from_matrix(rotm).as_quat()


def q2R(quat):
    rotation = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
    return rotation.as_matrix()


def read_and_process(input_file):
    data = []
    bottom = np.array([0.0, 0.0, 0.0, 1.0]).reshape([1, 4])
    with open(input_file, "r") as f:
        for line in f:
            if not line.startswith("#"):
                entry = parse_line(line)
                quat = entry["q_NtoC"]
                R = qvec2rotmat(quat)
                t = entry["p_NinC"]
                entry["R_NtoC"] = R
                m = np.concatenate([np.concatenate([R, t], 1), bottom], 0)  # R_WtoC
                T_CtoN = np.linalg.inv(m)
                entry["T_CtoN"] = T_CtoN
                entry["q_CtoN"] = rotmat2qvec(entry["T_CtoN"][0:3, 0:3])
                entry["p_CinN"] = entry["T_CtoN"][0:3, 3]
                data.append(entry)

    data.sort(key=lambda x: x["timestamp"])  # Sort by timestamp
    return data


def transform_data(data, q_NtoG, p_NinG, s_NtoG):
    for d in data:
        d["q_CtoG"] = R.from_matrix(
            np.matrix(R.from_quat(q_NtoG).as_matrix())
            * np.matrix(R.from_quat(d["q_CtoN"]).as_matrix())
        ).as_quat()
        d["p_CinG"] = np.array(
            s_NtoG
            * R.from_quat(q_NtoG).as_matrix()
            * np.matrix(d["p_CinN"]).reshape([3, 1])
            + p_NinG.reshape([3, 1])
        ).flatten()


def write_processed_data_inN(output_file, data):
    with open(output_file, "w") as f:
        f.write("# q_CtoN(Hamilton)\n")
        f.write("# p_CinN\n")
        f.write("# timestamp tx ty tz qx qy qz qw\n")
        for entry in data:
            timestamp_str = "{:.9f}".format(entry["timestamp"])
            p_CinN_str = " ".join("{:.6f}".format(x) for x in entry["p_CinN"])
            q_CtoN_str = " ".join("{:.6f}".format(x) for x in entry["q_CtoN"])
            f.write(f"{timestamp_str} {p_CinN_str} {q_CtoN_str}\n")


def write_processed_data_inG(output_file, data):
    with open(output_file, "w") as f:
        f.write("# q_CtoG(Hamilton)\n")
        f.write("# p_CinG\n")
        f.write("# timestamp tx ty tz qx qy qz qw\n")
        for entry in data:
            timestamp_str = "{:.9f}".format(entry["timestamp"])
            p_CinG_str = " ".join("{:.6f}".format(x) for x in entry["p_CinG"])
            q_CtoG_str = " ".join("{:.6f}".format(x) for x in entry["q_CtoG"])
            f.write(f"{timestamp_str} {p_CinG_str} {q_CtoG_str}\n")


def read_transform_data(filename):
    with open(filename, "r") as file:
        for line in file:
            if not line.startswith("#"):
                parts = line.split()
                # Hamilton
                q_NtoG = np.array([float(parts[i]) for i in range(0, 4)])
                p_NinG = np.array([float(parts[i]) for i in range(4, 7)])
                s_NtoG = float(parts[7])
                break

    print("q_NtoG:", q_NtoG)
    print("p_NinG:", p_NinG)
    print("s_NtoG:", s_NtoG)
    print()

    return np.array(q_NtoG), np.array(p_NinG), np.array(s_NtoG)


if __name__ == "__main__":
    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--transform_path", type=Path, required=True)
    parser.add_argument("--orig_result_path", type=Path, required=True)
    parser.add_argument("--vlresult_path", type=Path, required=True)
    parser.add_argument("--ovresult_path", type=Path, required=True)
    args = parser.parse_args().__dict__

    # read in transform
    q_NtoG, p_NinG, s_NtoG = read_transform_data(args["transform_path"])

    # read in visual localization result
    processed_data = read_and_process(args["orig_result_path"])
    transform_data(processed_data, q_NtoG, p_NinG, s_NtoG)

    # write visual localization result both in N frame (map frame) and in G frame (vicon frame)
    write_processed_data_inN(args["vlresult_path"], processed_data)
    write_processed_data_inG(args["ovresult_path"], processed_data)
    print("Processed data written done")
