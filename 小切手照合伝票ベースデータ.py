import os
import csv
from collections import defaultdict

# 输入文件路径
folder_path = r'\\133.220.10.118\share\システム課\01_システム管理ファイル\馬\小切手照合\小切手データ'  # 替换为你的文件夹路径
file_name = 'O20250415104806ZDATA.CSV'
file_path = os.path.join(folder_path, file_name)

# 输出文件路径
output_folder = r'\\133.220.10.118\share\システム課\01_システム管理ファイル\馬\小切手照合\導出データ'  # 替换为你的目标文件夹路径
output_file = os.path.join(output_folder, "伝票ベース最新版4月15日分.txt")

# 检查输出文件夹是否存在，不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 检查输入文件是否存在
if not os.path.isfile(file_path):
    print(f"文件未找到: {file_path}")
else:
    # 打开CSV文件并读取内容
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # 提取第33列和第30列从第58行开始的内容，同时提取第33列的倒数五位数字
    data_33_30 = defaultdict(list)
    for row in rows[109:]:  # 从第58行开始
        column_33_value = row[32][-5:]  # 提取倒数五位数字
        column_30_value = row[29]  # 第30列是索引为29的列
        column_14_value = row[14]
        column_13_value = row[13]
        column_5_value = row[4]
        column_1_value = row[1]

        data_33_30[column_1_value].append(
            [column_14_value, column_5_value, column_33_value, column_13_value, column_30_value, column_1_value]
        )

    # 将结果保存到文本文件中
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("日付順:\n")
        for key in sorted(data_33_30.keys()):  # 对键进行排序
            f.write(f"日付け: {key}\n")

            # 用于存储C列相同的行，E列值相加的结果
            combined_data = defaultdict(lambda: [None, None, None, None, 0, None])

            for item in data_33_30[key]:
                column_33_value = item[2]
                if combined_data[column_33_value][0] is None:
                    combined_data[column_33_value] = item
                else:
                    combined_data[column_33_value][4] = str(
                        int(float(combined_data[column_33_value][4]) + float(item[4]))
                    )  # E列相加，并去除“.0”

            for combined_item in combined_data.values():
                f.write(str(combined_item) + "\n")

    print(f"结果已保存到: {output_file}")
