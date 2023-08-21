import os
import sys
import math


def read_bad_timestamps(filename):
    bad_timestamps = []
    with open(filename, "r") as file:
        for line in file:
            bad_timestamps.append(float(line.strip()))
    return bad_timestamps


def is_timestamp_within_range(timestamp, bad_timestamps, threshold=0.005):
    for bad_timestamp in bad_timestamps:
        if math.isclose(timestamp, bad_timestamp, rel_tol=0, abs_tol=threshold):
            # print(timestamp)
            # print(bad_timestamp)
            return True
    return False


def filter_data(input_filename, output_filename, bad_timestamps, threshold=0.005):
    bad = 0
    total = 0
    with open(input_filename, "r") as input_file, open(
        output_filename, "w"
    ) as output_file:
        for line in input_file:
            if not line.startswith("#"):
                total += 1
                parts = line.strip().split()
                timestamp = float(parts[0])
                if not is_timestamp_within_range(timestamp, bad_timestamps, threshold):
                    output_file.write(line + "\n")  # Add a newline character
                else:
                    bad += 1
    print("bad/total: %d/%d" % (bad, total))


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python script.py bad_timestamps.txt input_data.txt output_data.txt"
        )
        return

    bad_timestamps_filename = sys.argv[1]
    input_data_filename = sys.argv[2]
    output_data_filename = sys.argv[3]

    if not os.path.exists(os.path.dirname(output_data_filename)):
        os.makedirs(os.path.dirname(output_data_filename))

    bad_timestamps = read_bad_timestamps(bad_timestamps_filename)
    filter_data(input_data_filename, output_data_filename, bad_timestamps)

    print("Filtered data written to", output_data_filename)


if __name__ == "__main__":
    main()
