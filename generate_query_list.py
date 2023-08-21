import os


def generate_txt(folder_path, output_file):
    # time_offset = int(0.002524377913673846 * 1e9)
    # print("time_offset: %d" % time_offset)
    with open(output_file, "w") as f:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_name = file
                    # f.write(
                    #     f"{image_name} OPENCV 848 480 416.85223429743274 414.92069080087543 421.02459311003213 237.76180565241077 -0.045761895748285604 0.03423951132164367 -0.00040139057556727315 0.000431371425853453\n"
                    # )
                    f.write(
                        f"{image_name} OPENCV 848 480 422.1242743871908 421.454264718481 421.48944391515926 237.80948220847125 -0.03756321381414493 0.030496333636595603 -0.0007748266172880399 0.0004432644578671401\n"
                    )


if __name__ == "__main__":
    for i in range(1, 9):
        folder_path = "/home/yuxiang/datasets/rpng_table/table_0" + str(i) + "_imgs"
        output_file = (
            "/home/yuxiang/workspace/Hierarchical-Localization/query_list/table_0"
            + str(i)
            + "_colmap_intrinsic.txt"
        )
        generate_txt(folder_path, output_file)
        print(f"Image names written to {output_file}")
