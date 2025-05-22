import os

def rename_files(folder_path, file_extension, start_idx=1):
    files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]
    files.sort()

    for idx, filename in enumerate(files, start=start_idx):
        new_name = f"{idx:03d}{file_extension}"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

paths = [
    ("DataSet/images/Trainadd", ".jpg", 301),
    ("DataSet/images/valadd", ".jpg", 101),
]

for path, ext, start in paths:
    rename_files(path, ext, start)
