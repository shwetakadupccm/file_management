import os
import numpy as np
import pandas as pd
import datetime

folder_path = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2014-June2019'
folder_path1 = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2019 IMAGES'
folder_path2 = 'Z:\\Clinical_Database\\surgery_ot_data'

folder_names = os.listdir(folder_path)

def get_summary_dir_subdir(folder_path):
    files_summary = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            dir_path = os.path.dirname(file_path)
            file_size = os.stat(file_path).st_size/float(1 << 20)
            file_size_rounded = round(file_size, 1)
            file_paths_name = np.append(dir_path, file)
            file_dat = np.append(file_paths_name, file_size_rounded)
            files_summary.append(file_dat)
            file_df = pd.DataFrame(files_summary, columns=['directory_path', 'file_name', 'file_size_in_MB'])
            print(file, file_size)
    return file_df

df = get_summary_dir_subdir(folder_path)
df.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(2014-2019)_sk.xlsx', index=False)

df1 = get_summary_dir_subdir(folder_path1)
df1.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(2019)_sk.xlsx', index=False)

df2 = get_summary_dir_subdir(folder_path2)
df2.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(ot_data_2021)_sk.xlsx', index=False)

def get_summary_dir_subdir(folder_path):
    files_summary = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.stat(file_path).st_size/float(1 << 20)
            file_size_rounded = round(file_size, 1)
            file_info = np.append(file_path, file)
            file_dat = np.append(file_info, file_size_rounded)
            files_summary.append(file_dat)
            file_df = pd.DataFrame(files_summary, columns=['path', 'file_name', 'file_size_in_MB'])
            print(file, file_size)
    return file_df

def get_file_name_size_time(file):
    file_size = file.stat().st_size/float(1 << 20)
    file_cr_time = datetime.datetime.fromtimestamp(file.stat().st_ctime)
    file_mo_time = datetime.datetime.fromtimestamp(file.stat().st_mtime)
    # print(file_size, file_cr_time, file_mo_time)
    file_name_size = np.append(file.name, file_size)
    file_cr_mo = np.append(file_cr_time, file_mo_time)
    output_lst = np.append(file_name_size, file_cr_mo)
    return output_lst

def get_file_name_size_if_dir(directory):
    file_data_from_dir = []
    file_names = os.scandir(directory)
    for file_name in file_names:
        if file_name.is_file():
            if os.path.exists(file_name):
                output_lst = get_file_name_size_time(file_name)
                file_data_from_dir.append(output_lst)
            else:
                output_lst = [file_name.name, 'not_exist', 'not_exist', 'not_exist']
                file_data_from_dir.append(output_lst)
    return file_data_from_dir

def get_output_df(folder_path):
    output_lst = []
    folder_names = os.scandir(folder_path)
    for folder_name in folder_names:
        file_path = os.path.join(folder_path, folder_name)
        print(file_path)
        if folder_name.is_file():
            lst = get_file_name_size_time(folder_name)
            lst1 = np.append(file_path, lst)
            output_lst.append(lst1)
        elif folder_name.is_dir():
            if os.path.exists(folder_name):
                file_path1 = os.path.join(folder_path, folder_name)
                print(file_path1)
                lst = get_file_name_size_if_dir(folder_name)
                lst1 = np.append(file_path1, lst)
                output_lst.append(lst1)
            else:
                file_path2 = os.path.join(folder_path, folder_name)
                print(file_path2)
                lst = [file_path2, folder_name.name, 'not_exist', 'not_exist', 'not_exist']
                output_lst.append(lst)
                try:
                    output_df = pd.DataFrame(output_lst, columns=['path', 'file_name', 'file_size_in_MB', 'file_created_date_time',
                                                      'file_modified_date_time'])
                except ValueError:
                    print('done')
    return output_df

output_df = get_output_df(folder_path)
##
def get_output_df1(folder_path):
    output_lst = []
    folder_names = os.scandir(folder_path)
    for folder_name in folder_names:
        file_path = os.path.join(folder_path, folder_name)
        print(file_path)
        if folder_name.is_file():
            lst = get_file_name_size_time(folder_name)
            lst1 = np.append(file_path, lst)
            output_lst.append(lst1)
        elif folder_name.is_dir():
            if os.path.exists(folder_name):
                file_path1 = os.path.join(folder_path, folder_name)
                print(file_path1)
                lst = get_file_name_size_if_dir(folder_name)
                lst1 = np.append(file_path1, lst)
                output_lst.append(lst1)
            else:
                file_path2 = os.path.join(folder_path, folder_name)
                print(file_path2)
                lst = [file_path2, folder_name.name, 'not_exist', 'not_exist', 'not_exist']
                output_lst.append(lst)
                try:
                    output_df = pd.DataFrame(output_lst, columns=['path', 'file_name', 'file_size_in_MB', 'file_created_date_time',
                                                      'file_modified_date_time'])
                except ValueError:
                    print('done')
    return output_df
##





# def get_directory_size(directory):
#     total = 0
#     try:
#         # print("[+] Getting the size of", directory)
#         for entry in os.scandir(directory):
#             if entry.is_file():
#                 # if it's a file, use stat() function
#                 total += entry.stat().st_size
#             elif entry.is_dir():
#                 # if it's a directory, recursively call this function
#                 total += get_directory_size(entry.path)
#     except NotADirectoryError:
#         # if `directory` isn't a directory, get the file size then
#         return os.path.getsize(directory)
#     except PermissionError:
#         # if for whatever reason we can't open the folder, return 0
#         return 0
#     return total
