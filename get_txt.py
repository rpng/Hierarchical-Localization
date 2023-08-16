import os


def generate_txt(folder_path, output_file):
    with open(output_file, "w") as f:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_name = file
                    f.write(
                        f"{image_name} OPENCV 480 848 416.85223429743274 414.92069080087543 421.02459311003213 237.76180565241077 -0.045761895748285604 0.03423951132164367 -0.00040139057556727315 0.000431371425853453\n"
                    )


if __name__ == "__main__":
    folder_path = "/home/yuxiang/datasets/rpng_table/table_02_imgs"
    output_file = "output2.txt"
    generate_txt(folder_path, output_file)
    print(f"Image names written to {output_file}")
