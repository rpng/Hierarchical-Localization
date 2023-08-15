import os


def generate_txt(folder_path, output_file):
    with open(output_file, 'w') as f:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_name = file
                    f.write(
                        f"{image_name} OPENCV 480 848 422.22392478751 421.5837091770003 421.63836802402244 237.8020266067116 -0.03762828417477932 0.0305696166414784 -0.0007886943489785149 0.0005470674577582285\n")


if __name__ == "__main__":
    folder_path = "/home/tim/datasets/rpng_table/table_01_imgs"
    output_file = "output.txt"
    generate_txt(folder_path, output_file)
    print(f"Image names written to {output_file}")
