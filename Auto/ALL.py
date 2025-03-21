import os
import zipfile
import datetime
import shutil
import glob

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
destination_folder2 = "【下载看这里】合集下载"


def zip_json_files(_source_folder, _destination_file):
    with zipfile.ZipFile(_destination_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(_source_folder):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=os.path.relpath(file_path, _source_folder))


def check_file_exists(pattern):
    matching_files = glob.glob(pattern)
    if len(matching_files) > 0:
        for file_name in matching_files:
            os.remove(file_name)
            print(f"Removed {file_name}")


def count_files_in_directory(directory):
    return sum([len(files) for r, d, files in os.walk(directory)])


source_list = ["插曲", "别传"]

for source in source_list:

    source_folder_base = f"插曲&别传/{source}"
    destination_folder = f"插曲&别传/{source}/压缩包"

    # 遍历需要压缩的文件夹并进行压缩
    for folder_name in os.listdir(source_folder_base):
        if folder_name.startswith(source):
            # 构造源文件夹和目标压缩包文件路径
            source_folder_path = os.path.join(source_folder_base, folder_name)
            destination_zip_path = os.path.join(destination_folder, folder_name + ".zip")

            # 如果目标文件夹中已经存在同名的文件，先删除它
            if os.path.exists(destination_zip_path):
                os.remove(destination_zip_path)

            # 进行压缩
            shutil.make_archive(destination_zip_path[:-4], 'zip', source_folder_path)

            # 输出提示信息
            print(f"成功压缩文件夹{source_folder_path}为压缩包{destination_zip_path}")

    # 创建一个临时目录来存放要压缩的文件夹
    temp_dir = os.path.join(destination_folder, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    subfolders = [f.path for f in os.scandir(source_folder_base) if f.is_dir() and f.name != '压缩包']
    # 将所有要压缩的文件夹复制到临时目录
    for subfolder in subfolders:
        shutil.copytree(subfolder, os.path.join(temp_dir, os.path.basename(subfolder)))

    # 创建压缩文件
    shutil.make_archive(os.path.join(destination_folder2, source), 'zip', temp_dir)

    # 删除临时目录
    shutil.rmtree(temp_dir)

    print(f"成功压缩文件夹到 '{os.path.join(destination_folder2, f'{source}.zip')}'")

source2_list = ["往期剿灭", "模组任务", "悖论模拟", "资源关"]

for source_folder in source2_list:
    check_file_exists(f"【下载看这里】合集下载/{source_folder}-*")
    total_files = count_files_in_directory(source_folder)
    destination_file = os.path.join("【下载看这里】合集下载",
                                    os.path.basename(source_folder) + "-" + str(total_files) + ".zip")
    # 压缩指定类型文件
    zip_json_files(source_folder, destination_file)
    print(f"成功压缩{destination_file}")

check_file_exists("【下载看这里】合集下载/【当前活动】*")
# 当前活动
now_activity_folders = glob.glob("【当前活动】*")
# 遍历所有匹配的文件夹
for folder in now_activity_folders:
    # 构造目标压缩文件的路径
    destination_file = os.path.join("【下载看这里】合集下载", os.path.basename(folder) + ".zip")
    # 如果目标文件存在，就删除它
    if os.path.exists(destination_file):
        os.remove(destination_file)

    # 压缩文件夹
    shutil.make_archive(destination_file[:-4], 'zip', folder)

    print(f"成功压缩{folder}为{destination_file}")
# ALL
folders = [
    "资源关",
    "主线",
    "往期剿灭",
    "模组任务",
    "插曲&别传",
    "悖论模拟"
] + [folder for folder in now_activity_folders]

# 指定目标文件夹路径
target_dir = "【下载看这里】合集下载"
check_file_exists("【下载看这里】合集下载/ALL-*")
# 生成压缩文件名
zip_file_name = "ALL-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".zip"

# 压缩文件夹
zip_file_path = os.path.join(target_dir, zip_file_name)
with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, os.path.dirname(folder)))

# 移动压缩文件到目标文件夹
shutil.move(zip_file_path, os.path.join(target_dir, zip_file_name))
print(f"所有文件已成功压缩为: {os.path.join(target_dir, zip_file_name)}")
