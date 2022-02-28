import pandas as pd
import os
import shutil

sub_dirs_2021 = pd.read_excel('D:\\Shweta\\surgery_images_ss\\2021_07_21_sub_dirs_2021_sk_dk.xlsx')

file_num_na_data = sub_dirs_2021[sub_dirs_2021['file_number'].isnull()][0:101]
file_num_na_data.to_excel('D:\\Shweta\\surgery_images_ss\\trial_files_sk\\2021_22_07_trial_file_2021_sx_img_sk.xlsx', index=False)

def patient_name_cleaning(df, patient_name_str):
    cleaned_patient_names = []
    for patient_name in df[patient_name_str]:
        cleaned_patient_name = patient_name.lower()
        cleaned_patient_name = cleaned_patient_name.replace(' ', '_')
        cleaned_patient_names.append(cleaned_patient_name)
    return cleaned_patient_names

def create_folder_name(df, patient_name_str, file_num_str):
    folder_new_names = []
    df['cleaned_patient_name'] = patient_name_cleaning(df, patient_name_str)
    for i in range(len(df)):
        clean_patient_name = df.iloc[i]['cleaned_patient_name']
        file_number = df.iloc[i][file_num_str]
        new_name = clean_patient_name + '_' + file_number
        folder_new_names.append(new_name)
    return folder_new_names

###
def copy_and_rename_the_folder_file(detsination_image_folder, destination_video_folder, excel_file,
                                    dir_path_str='directory_path', old_file_name_str = 'file_name',
                                    repo_file_name_str='repo_file_name', folder_str='folder'):

    for index, dir_path in enumerate(excel_file[dir_path_str]):
        source_path = dir_path
        source_file_name = excel_file.iloc[index][old_file_name_str]
        dir_file_type = excel_file.iloc[index][folder_str]
        if dir_file_type == 'image':
            image_new_name = excel_file.iloc[index][repo_file_name_str]
            print(image_new_name)
            source_image_path = os.path.join(source_path, source_file_name)
            detsination_image_path = os.path.join(detsination_image_folder, image_new_name)
            shutil.copy(source_image_path, detsination_image_path)
        elif dir_file_type == 'video':
            video_new_name = excel_file.iloc[index][repo_file_name_str]
            print(video_new_name)
            source_video_path = os.path.join(source_path, source_file_name)
            destination_video_path = os.path.join(destination_video_folder, video_new_name)
            shutil.copy(source_video_path, destination_video_path)

destination_path = 'D:\\Shweta\\surgery_images_ss'
detsination_image_folder = 'D:\\Shweta\\surgery_images_ss\\images'
destination_video_folder = 'D:\\Shweta\\surgery_images_ss\\videos'

copy_and_rename_the_folder_file(detsination_image_folder, destination_video_folder, file_num_na_data,
                                    dir_path_str='directory_path', old_file_name_str= 'file_name',
                                    repo_file_name_str='repo_file_name', folder_str='folder')

##

