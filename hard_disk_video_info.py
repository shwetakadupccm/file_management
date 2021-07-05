import os
import numpy as np
import pandas as pd
import re

folder_path = 'F:\\Videos to be seen by Dr.Koppiker'

def get_summary_dir_subdir(folder_path):
    files_summary = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            try:
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
            except FileNotFoundError:
                print('error')
    return file_df

video_summary_df = get_summary_dir_subdir(folder_path)
video_summary_df.to_excel('D:\\video_summary_sk.xlsx', index=False)

def split_dir_path(df, dir_path_name_str = 'directory_path',
                   parent_folder_path = 'F:\\Videos to be seen by Dr.Koppiker',
                   substring = '\\'):
    spllited_dir = []
    for dir_path in df[dir_path_name_str]:
        child_dir = dir_path.replace(parent_folder_path, '')
        split_dir = child_dir.replace(substring, ',')
        spllited_lst = re.split(',', split_dir)
        print(spllited_lst)
        spllited_dir.append(spllited_lst)
        output_df = pd.DataFrame(spllited_dir, columns=['dir_name', 'dir_name1', 'dir_name2', 'dir_name3', 'dir_name4', 'dir_name5',
                                                        'dir_name6', 'dir_name7', 'dir_name8'])
    return output_df

video_df = pd.read_excel('D:\\video_summary_sk.xlsx')

df = split_dir_path(video_df, dir_path_name_str = 'directory_path',
                   parent_folder_path = 'F:\\Videos to be seen by Dr.Koppiker',
                   substring = '\\')

final_df = pd.concat([video_df, df], axis=1)
final_df.to_excel('D:\\Shweta\\surgery_images_ss\\video_excel\\2021_05_07_surgery_video_summary_sk.xlsx', index=False)
