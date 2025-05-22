import os


def rename_files(folder_path, file_extension):
    # 获取文件夹内所有指定格式的文件
    files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]
    files.sort()  # 按原始文件名排序

    for idx, filename in enumerate(files, start=1):
        # 生成新文件名（如 001.jpg）
        new_name = f"{idx:03d}{file_extension}"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        # 重命名文件
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")


# 需要重命名的路径（根据您的实际路径修改）
paths = [
    "DataSet1/images/train",  # 图像训练集
    "DataSet1/images/val",  # 图像验证集
    "DataSet1/labels/train",  # 标签训练集
    "DataSet1/labels/val"  # 标签验证集
]

# 执行重命名
for path in paths:
    if "images" in path:
        rename_files(path, ".jpg")  # 图像文件扩展名（根据实际调整）
    else:
        rename_files(path, ".xml")  # 标签文件扩展名