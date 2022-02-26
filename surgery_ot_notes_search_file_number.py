import os

import pandas as pd
import numpy as np
import re
from fuzzywuzzy import fuzz, process

ot_notes_df = pd.read_excel('D:\\Shweta\\surgery_ot_notes\\PCCM_Surgery_OT notes_10-03-2021_RB_RU_DA.xlsx')
master_file = pd.read_excel('D:\\Shweta\\Patient_name_matching\\master_list\\2010_2018_name_file_number_whole.xlsx')

ot_notes_df['full_name'] = ot_notes_df[ot_notes_df.columns[1:4]].apply(
    lambda x: ' '.join(x.dropna().astype(str)), axis = 1)


# def create_full_name(df, first_name_str, middle_name_str, last_name_str):
#     full_names = []
#     for i in range(len(df)):
#         full_name = df[i][first_name_str, middle_name_str, last_name_str].apply(
#             lambda x: ' '.join(x.dropna().astype(str)), axis = 1)
#         full_names.append(full_name)
#     return full_names

# names = create_full_name(ot_notes_df, first_name_str = 'First Name', middle_name_str = 'Middle Name', last_name_str = 'Last Name')

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        clean_name = re.sub('[^a-zA-Z]', ' ', str(name))
        clean_name = clean_name.lower()
        cleaned_names.append(clean_name)
    return cleaned_names

def find_file_number_from_master_list(master_df, ot_notes_df, master_name_str='patient_name',
                                      master_file_num_str='file_number', ot_notes_name_str='full_name'):
    master_cleaned_names = clean_names(master_df, master_name_str)
    ot_notes_clean_names = clean_names(ot_notes_df, ot_notes_name_str)
    matched_names = []

    for name in ot_notes_clean_names:
        matched_name = process.extractOne(query=name, choices=master_cleaned_names, scorer=fuzz.token_set_ratio)
        if matched_name is not None:
            master_name_index = master_cleaned_names.index(matched_name[0])
            master_cols = [master_name_str, master_file_num_str]
            master_dat = master_df.iloc[master_name_index][master_cols]
            lst = np.append(name, master_dat)
            matched_names.append(lst)
            output_df = pd.DataFrame(matched_names, columns= ['patient_name_from_ot_list', 'patient_name_from_master', 'file_number'])
    return output_df

df = find_file_number_from_master_list(master_file, ot_notes_df, master_name_str='patient_name',
                                      master_file_num_str='file_number', ot_notes_name_str='full_name')

df.to_excel('D:\\Shweta\\surgery_ot_notes\\master_ot_patient_names_file_nums.xlsx', index=False)

### surgery ot data info
import os

folder_path = 'Z:/Clinical_Database/Digitized_Files/Surgery_data_raw/Surgery_OT_Notes/Jehangir_OT_data_date_wise_and_patient_names_till_30_09_2021_sk'

def get_summary_dir_subdir(folder_path):
    files_summary = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            dir_path = os.path.dirname(file_path)
            dir_name = os.path.dirname(dir_path)
            print(dir_name)
            file_paths_name = [dir_path, file]
            files_summary.append(file_paths_name)
    file_df = pd.DataFrame(files_summary, columns=['directory_path', 'file_name'])
    return file_df

df = get_summary_dir_subdir(folder_path)

def split_dir_path(df, dir_path_name_str = 'directory_path',
                   parent_folder_path = 'Z:/Clinical_Database/Digitized_Files/Surgery_data_raw/Surgery_OT_Notes/Jehangir_OT_data_date_wise_and_patient_names_till_30_09_2021_sk',
                   substring = '\\'):
    spllited_dir = []
    for dir_path in df[dir_path_name_str]:
        child_dir = dir_path.replace(parent_folder_path, '')
        split_dir = child_dir.replace(substring, ',')
        spllited_lst = re.split(',', split_dir)
        print(spllited_lst)
        spllited_dir.append(spllited_lst)
        output_df = pd.DataFrame(spllited_dir, columns=['dir_name', 'dir_name1', 'dir_name2'])
    return output_df

output_df = split_dir_path(df, dir_path_name_str = 'directory_path',
                   parent_folder_path = 'Z:/Clinical_Database/Digitized_Files/Surgery_data_raw/Surgery_OT_Notes/Jehangir_OT_data_date_wise_and_patient_names_till_30_09_2021_sk',
                   substring = '\\')

output_df.to_excel('D:/Shweta/surgery_ot_notes/ot_folder_info/2022_02_10_ot_sx_data_dir_info.xlsx', index=False)

dir_info = []
file_info = []
for roots, dirs, files in os.walk(folder_path):
    for dir in dirs:
        print(dir)
        dir_info.append(dir)
        for file in files:
            file_path = os.path.join(dir, file)
            file_info.append(file)

file_names = os.listdir(folder_path)
df = pd.DataFrame(file_names, columns=['dates'])
df.to_excel('D:/Shweta/surgery_ot_notes/ot_folder_info/2022_02_10_ot_sx_dates.xlsx', index=False)