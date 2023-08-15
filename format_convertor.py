import numpy as np
from scipy.spatial.transform import Rotation as R


def parse_line(line):
    parts = line.split()
    timestamp_str = parts[0].split(".")[0]  # Extract the timestamp part before '.png'
    timestamp = float(
        timestamp_str[:10] + "." + timestamp_str[10:]
    )  # Format the timestamp
    rotation = np.array([float(parts[i]) for i in range(1, 5)])
    translation = np.array([float(parts[i]) for i in range(5, 8)]).reshape([3, 1])
    return {"timestamp": timestamp, "rotation": rotation, "translation": translation}


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
                quat = entry["rotation"]
                R = qvec2rotmat(quat)
                t = entry["translation"]
                entry["rotation_matrix"] = R
                m = np.concatenate([np.concatenate([R, t], 1), bottom], 0)  # R_WtoC
                c2w = np.linalg.inv(m)
                entry["c2w"] = c2w
                entry["q_CtoG"] = rotmat2qvec(entry["c2w"][0:3, 0:3])
                entry["p_CinG"] = entry["c2w"][0:3, 3]
                data.append(entry)

    data.sort(key=lambda x: x["timestamp"])  # Sort by timestamp
    return data


def write_processed_data(output_file, data):
    with open(output_file, "w") as f:
        for entry in data:
            timestamp_str = "{:.9f}".format(entry["timestamp"])
            p_CinG_str = " ".join("{:.6f}".format(x) for x in entry["p_CinG"])
            q_CtoG_str = " ".join("{:.6f}".format(x) for x in entry["q_CtoG"])
            f.write(f"{timestamp_str} {p_CinG_str} {q_CtoG_str}\n")


if __name__ == "__main__":
    input_file = "outputs/sfm/hloc_superpoint+superglue_netvlad20.txt"
    processed_data = read_and_process(input_file)

    output_file = "processed_data.txt"
    write_processed_data(output_file, processed_data)
    print(f"Processed data written to {output_file}")
