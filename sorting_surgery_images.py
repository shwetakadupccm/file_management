import os
import numpy as np
import pandas as pd
import datetime
import re
import itertools

folder_path = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2014-June2019'
# folder_path1 = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2019 IMAGES'
# folder_path2 = 'Z:\\Clinical_Database\\surgery_ot_data'

folder_names = os.listdir(folder_path)

def get_summary_dir_subdir(folder_path):
    files_summary = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            dir_path = os.path.dirname(file_path)
            # dir_name = os.path.dirname(dir_path)
            # print(dir_name)
            file_size = os.stat(file_path).st_size/float(1 << 20)
            file_size_rounded = round(file_size, 1)
            file_paths_name = np.append(dir_path, file)
            file_dat = np.append(file_paths_name, file_size_rounded)
            files_summary.append(file_dat)
            file_df = pd.DataFrame(files_summary, columns=['directory_path', 'file_name', 'file_size_in_MB'])
            print(file)
    return file_df

# df = get_summary_dir_subdir(folder_path)
# df.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(2014-2019)_sk.xlsx', index=False)

df = pd.read_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(2014-2019)_sk.xlsx')

# df1 = get_summary_dir_subdir(folder_path1)
# df1.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(2019)_sk.xlsx', index=False)
#
# df2 = get_summary_dir_subdir(folder_path2)
# df2.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(ot_data_2021)_sk.xlsx', index=False)

dir_path = 'Y:\\RESEARCH\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2014-June2019\\Sunita Mali\\6-28-2016'

patterns = ['\d{4}-\d{2}-\d{2}', '\d{4}-\d{1}-\d{1}', '\d{4}-\d{2}-\d{1}', '\d{4}-\d{1}-\d{2}',
            '\d{2}-\d{2}-\d{4}', '\d{1}-\d{1}-\d{4}','\d{1}-\d{2}-\d{4}', '\d{2}-\d{1}-\d{4}',]

patterns_dict = {'%Y-%m-%d': ['\d{4}-\d{2}-\d{2}', '\d{4}-\d{1}-\d{1}', '\d{4}-\d{2}-\d{1}', '\d{4}-\d{1}-\d{2}'],
                 '%Y-%d-%m': ['\d{4}-\d{1}-\d{2}', '\d{4}-\d{1}-\d{1}', '\d{4}-\d{2}-\d{1}', '\d{4}-\d{1}-\d{2}'],
                 '%m-%d-%Y': ['\d{1}-\d{1}-\d{4}', '\d{1}-\d{2}-\d{4}', '\d{2}-\d{2}-\d{4}', '\d{2}-\d{1}-\d{4}'],
                 '%d-%m-%Y': ['\d{2}-\d{1}-\d{4}', '\d{2}-\d{2}-\d{4}', '\d{1}-\d{1}-\d{4}', '\d{1}-\d{2}-\d{4}']
                 }

def get_value_from_key(pattern_dict, value):
    id_pos = [value in value_list for value_list in (pattern_dict.values())]
    key_reqd = list(itertools.compress(pattern_dict.keys(), id_pos))
    return key_reqd

def get_matched_dt_pattern(patterns, patterns_dict, dir_path):
    matched_dts = []
    for pattern in patterns:
        match = re.search(pattern, str(dir_path))
        print(match)
        if match is not None:
            val = get_value_from_key(patterns_dict, pattern)
            # print(val)
            # print(len(val))
            if len(val) == 1:
                try:
                    dt = datetime.datetime.strptime(match.group(), val[0]).date()
                    matched_dts.append(dt)
                    # print(dt)
                except ValueError:
                    dt = datetime.datetime.strptime(match.group(), val[0][3:]).date()
                    matched_dts.append(dt)
                    # print(dt)
                except:
                    print('not_matched')
            elif len(val) == 2:
                try:
                    dt = datetime.datetime.strptime(match.group(), val[0]).date()
                    matched_dts.append(dt)
                    dt1 = datetime.datetime.strptime(match.group(), val[1]).date()
                    matched_dts.append(dt1)
                    # print(dt1)
                except ValueError:
                    dt = datetime.datetime.strptime(match.group(), val[0][3:]).date()
                    matched_dts.append(dt)
                    dt1 = datetime.datetime.strptime(match.group(), val[1][3:]).date()
                    matched_dts.append(dt1)
                    # print(dt1)
                except:
                    print('not_matched')
            elif len(val) == 3:
                try:
                    dt = datetime.datetime.strptime(match.group(), val[0]).date()
                    matched_dts.append(dt)
                    dt1 = datetime.datetime.strptime(match.group(), val[1]).date()
                    matched_dts.append(dt1)
                    # print(dt1)
                    dt2 = datetime.datetime.strptime(match.group(), val[2]).date()
                    matched_dts.append(dt2)
                    # print(dt2)
                except ValueError:
                    dt = datetime.datetime.strptime(match.group(), val[0][3:]).date()
                    matched_dts.append(dt)
                    dt1 = datetime.datetime.strptime(match.group(), val[1][3:]).date()
                    matched_dts.append(dt1)
                    # print(dt1)
                    dt2 = datetime.datetime.strptime(match.group(), val[2][3:]).date()
                    matched_dts.append(dt2)
                    # print(dt2)
                except:
                    print('not_matched')
    return matched_dts

matched_dts = get_matched_dt_pattern(patterns, patterns_dict, dir_path)

def get_sub_dirs_dates(patterns, patterns_dict, df, dir_name_str = 'directory_path'):
    dts = []
    for dir_path in df[dir_name_str]:
        print(dir_path)
        dt = get_matched_dt_pattern(patterns, patterns_dict, dir_path)
        dts.append(dt)
        print(dt)
    return dts

dts = get_sub_dirs_dates(patterns, patterns_dict, df, dir_name_str = 'directory_path')
df['image_dates'] = dts
df.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_24_extracted_dates_sk.xlsx')
pd.to_datetime(df.image_dates, '%m-%d-%Y')
##

def get_matched_dt_pattern(patterns, patterns_dict, dir_path):
    matched_dts = []
    for pattern in patterns:
        match = re.search(pattern, str(dir_path))
        print(match)
        if match is not None:
            val = get_value_from_key(patterns_dict, pattern)
            print(val)
            print(len(val))
            try:
                dt = datetime.datetime.strptime(match.group(), val[0]).date()
                matched_dts.append(dt)
                print(dt)
            except ValueError:
                dt1 = datetime.datetime.strptime(match.group(), val[1]).date()
                matched_dts.append(dt1)
                print(dt1)
            except:
                matched_dts.append('NA')
                print('error')
    return matched_dts


def get_matched_groups(patterns, dir_path):
    matched_patterns = []
    for pattern in patterns:
        print(pattern)
        match = re.search(pattern, str(dir_path))
        print(match)
        if match is not None:
            lst = np.append(match, pattern)
            matched_patterns.append(lst)
    return matched_patterns

dir_path = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2014-June2019\\Zubeida Shaikh(RC)\\10-12-2015'
matched_patterns = get_matched_groups(patterns, dir_path)

for matched_pattern in matched_patterns:
    val = get_value_from_key(patterns_dict, matched_pattern[0][0])
    print(matched_pattern, val)


# def get_matched_dt_pattern(patterns, patterns_dict, dir_path):
#     matched_dts = []
#     for pattern in patterns:
#         match = re.search(pattern, str(dir_path))
#         if match is not None:
#             val = get_value_from_key(patterns_dict, pattern)
#             # print(match, val)
#             try:
#                 dt = datetime.datetime.strptime(match.group(), val[0]).date()
#                 matched_dts.append(dt)
#             except ValueError:
#                 # try:
#                 #     '%d-%Y'
#                 matched_dts.append('not_available')
#             # print(dt)
#     return matched_dts


# def get_date_image(patterns, dir_path):
#     matched_dict = get_matched_dt_pattern(patterns, dir_path)
#     for matched_pattern in matched_dict.values():
#         if matched_pattern is not None:
#             val = get_value_from_key(matched_dict, matched_pattern)
#             print(val)
#             dt = datetime.datetime.strptime(val.group(), val[0]).date()
#             print(dt)
#             return dt
#         else:
#             return 'NA'
#
# get_date_image(patterns, dir_path)

# def get_sub_dirs_dates(patterns, patterns_dict, df, dir_name_str = 'directory_path'):
#     dts = []
#     for dir_path in df[dir_name_str]:
#         print(dir_path)
#         dt = get_matched_dt_pattern(patterns, patterns_dict, dir_path)
#         dts.append(dt)
#         print(dt)
#     return dts

# dts = get_sub_dirs_dates(patterns, patterns_dict, df, dir_name_str = 'directory_path')

# dir_path = 'Y:\RESEARCH\RESEARCH-TEAM\Smita Sister\All surgical images\2014-June2019\Vrushali Nalawade\8-7-2017'
# df['image_dates'] = dts


# def get_summary_dir_subdir(folder_path):
#     files_summary = []
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             file_size = os.stat(file_path).st_size/float(1 << 20)
#             file_size_rounded = round(file_size, 1)
#             file_info = np.append(file_path, file)
#             file_dat = np.append(file_info, file_size_rounded)
#             files_summary.append(file_dat)
#             file_df = pd.DataFrame(files_summary, columns=['path', 'file_name', 'file_size_in_MB'])
#             print(file, file_size)
#     return file_df

# def get_file_name_size_time(file):
#     file_size = file.stat().st_size/float(1 << 20)
#     file_cr_time = datetime.datetime.fromtimestamp(file.stat().st_ctime)
#     file_mo_time = datetime.datetime.fromtimestamp(file.stat().st_mtime)
#     # print(file_size, file_cr_time, file_mo_time)
#     file_name_size = np.append(file.name, file_size)
#     file_cr_mo = np.append(file_cr_time, file_mo_time)
#     output_lst = np.append(file_name_size, file_cr_mo)
#     return output_lst

# def get_file_name_size_if_dir(directory):
#     file_data_from_dir = []
#     file_names = os.scandir(directory)
#     for file_name in file_names:
#         if file_name.is_file():
#             if os.path.exists(file_name):
#                 output_lst = get_file_name_size_time(file_name)
#                 file_data_from_dir.append(output_lst)
#             else:
#                 output_lst = [file_name.name, 'not_exist', 'not_exist', 'not_exist']
#                 file_data_from_dir.append(output_lst)
#     return file_data_from_dir

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
