import numpy as np
import pandas as pd
import re
import datetime

df = pd.read_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(2014-2019)_sk.xlsx')
df1 = pd.read_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(2019)_sk.xlsx')
df2 = pd.read_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_23_surgery_images_info(ot_data_2021)_sk.xlsx')

# string = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2014-June2019\\2014\\12-13-2014'
# splitted_str = string.replace(folder_path, '')
#
# substring = '\\'
# lst = splitted_str.replace(substring, ',')
# lst1 = re.split(',', lst)

def split_dir_path(df, dir_path_name_str = 'directory_path',
                   parent_folder_path = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2014-June2019\\',
                   substring = '\\'):
    spllited_dir = []
    bracket_info_lst = []
    for dir_path in df[dir_path_name_str]:
        child_dir = dir_path.replace(parent_folder_path, '')
        split_dir = child_dir.replace(substring, ',')
        spllited_lst = re.split(',', split_dir)
        print(spllited_lst)
        lenght = len(spllited_lst)
        print(lenght)
        bracket_info_gr = re.search(r"\(([-A-Za-z0-9_ ]+)\)", dir_path)
        if bracket_info_gr is not None:
            bracket_info = bracket_info_gr.group(1)
            print(bracket_info)
            bracket_info_lst.append(bracket_info)
        else:
            bracket_info_lst.append('nothing_in_brackets')
        len_lst = np.append(lenght, spllited_lst)
        spllited_dir.append(len_lst)
        output_df = pd.DataFrame(spllited_dir, columns=['length', 'dir_name', 'dir_name1', 'dir_name2', 'dir_name3', 'dir_name4', 'dir_name5'])
        output_df.insert(0, 'info_from_brackets', bracket_info_lst)
    return output_df

output_df = split_dir_path(df, dir_path_name_str = 'directory_path',
                   parent_folder_path = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2014-June2019\\',
                   substring = '\\')

final_df = pd.concat([df, output_df], axis=1)
final_df.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_25_sub_dirs(2014-2019)_sk.xlsx', index=False)

##
output_df1 = split_dir_path(df1, dir_path_name_str = 'directory_path',
                   parent_folder_path = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2019 IMAGES\\',
                   substring = '\\')

final_df1 = pd.concat([df1, output_df1], axis=1)
final_df1.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_25_sub_dirs(2019)_sk.xlsx', index=False)
##
def split_dir_path_for_2021(df, dir_path_name_str = 'directory_path',
                   parent_folder_path = 'Y:\\RESEARCH\\RESEARCH-TEAM\\Smita Sister\\All surgical images\\2014-June2019\\',
                   substring = '\\', date_digit_pattern = '\d{8}'):
    spllited_dir = []
    bracket_info_lst = []
    video_dates = []
    for dir_path in df[dir_path_name_str]:
        child_dir = dir_path.replace(parent_folder_path, '')
        split_dir = child_dir.replace(substring, ',')
        spllited_lst = re.split(',', split_dir)
        print(spllited_lst)
        lenght = len(spllited_lst)
        print(lenght)
        bracket_info_gr = re.search(r"\(([-A-Za-z0-9_ ]+)\)", dir_path)
        if bracket_info_gr is not None:
            bracket_info = bracket_info_gr.group(1)
            print(bracket_info)
            bracket_info_lst.append(bracket_info)
        else:
            bracket_info_lst.append('nothing_in_brackets')
        int_gr = re.search(date_digit_pattern, dir_path)
        if int_gr is not None:
            dt = datetime.datetime.strptime(int_gr.group(), '%Y%m%d').date()
            video_dates.append(dt)
        else:
            video_dates.append('date_not_available')
        len_lst = np.append(lenght, spllited_lst)
        spllited_dir.append(len_lst)
        output_df = pd.DataFrame(spllited_dir, columns=['length', 'dir_name', 'dir_name1', 'dir_name2', 'dir_name3', 'dir_name4',
                                                        'dir_name5', 'dir_name6'])
        output_df.insert(0, 'info_from_brackets', bracket_info_lst)
        output_df.insert(1, 'video_date', video_dates)
    return output_df

output_df2 = split_dir_path_for_2021(df2, dir_path_name_str = 'directory_path',
                   parent_folder_path = 'Z:\\Clinical_Database\\surgery_ot_data\\',
                   substring = '\\', date_digit_pattern = '\d{8}')

final_df2 = pd.concat([df2, output_df2], axis=1)

final_df2.to_excel('D:\\Shweta\\surgery_images_ss\\output_df\\2021_06_30_sub_dirs(2021).xlsx', index=False)

##
string = 'Y:\RESEARCH\RESEARCH-TEAM\Smita Sister\All surgical images\2014-June2019\Aarti BBay (RC)'
string = 'Y:\RESEARCH\RESEARCH-TEAM\Smita Sister\All surgical images\2014-June2019\Anita Baheti( RC-skin sparing)'

result = re.search(r"\(([-A-Za-z0-9_ ]+)\)", string)
print(result.group(1))

# 'U+2702' or 'U+0022'

##
# string_pattern = '\d{8}'
# string1 = 'Z:\\Clinical_Database\\surgery_ot_data\\2021_05\\CHANCHALABAI OSTWAL\\20210514100306_903063\\video_files'
# gr = re.search(string_pattern, string1)
# dt = datetime.datetime.strptime(gr.group(), '%Y%m%d').date()
# dt