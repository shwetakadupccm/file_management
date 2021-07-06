import os
import pandas as pd
import shutil
import re

lines = []
file = open('D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt\\ANIL_DEVGAN_[_fnac].txt', 'rt')

# patient_name = []
# date = []
# pattern = re.compile("mr", re.IGNORECASE)  # Compile a case-insensitive regex
# pattern1 = re.compile("ms", re.IGNORECASE)
# pattern2 = re.compile('\d{2}/\d{2}/\d{4}')
# with open ('D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt\\ANIL_DEVGAN_[_fnac].txt', 'rt') as myfile:
#     for line in myfile:
#         if pattern.search(line) != None:
#             patient_name.append(line.rstrip('\n'))
#             print(line)
#         elif pattern1.search(line) != None:
#             patient_name.append(line.rstrip('\n'))
#             print(line)
#         elif pattern2.search(line) != None:
#             date.append(line.rstrip('\n'))
#             print(line)
##

def get_patient_name_surgery_date(file, str1 = 'mr', str2 = 'ms', str3 = '\d{2}/\d{2}/\d{4}'):
    pattern1 = re.compile(str1, re.IGNORECASE)
    pattern2 = re.compile(str2, re.IGNORECASE)
    pattern3 = re.compile(str3)
    patient_names = []
    dates = []
    for line in file:
        if pattern1.search(line) != None:
            patient_names.append(line.rstrip('\n'))
            print(line)
        elif pattern2.search(line) != None:
            patient_names.append(line.rstrip('\n'))
            print(line)
        elif pattern3.search(line) != None:
            dates.append(line.rstrip('\n'))
            print(line)
    return patient_names, dates

patient_names, dates = get_patient_name_surgery_date(file, str1 = 'mr', str2 = 'ms', str3 = '\d{2}/\d{2}/\d{4}')

string = 'chemotherapy'

##
folder_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt'
destination_path = 'D:\\Shweta\\path_reports\\chemo_path_reports'

def read_file_text(folder_path, string = 'chemotherapy', str1 = 'mr', str2 = 'ms', str3 = '\d{2}/\d{2}/\d{4}'):
    file_names = os.listdir(folder_path)
    patient_names = []
    dates = []
    reports_name = []
    for file_name in file_names:
        file = open(folder_path + '\\' + file_name, 'rt')
        file_text = file.read()
        file_text.lower()
        if string in file_text:
            print('string_is_there')
            reports_name.append(file_name)
            patient_name, dts = get_patient_name_surgery_date(file, str1, str2, str3)
            print(patient_name)
            print(dts)
            patient_names.append(patient_name)
            dates.append(dts)
        else:
            print('string_is_not_there')
    output_df = pd.DataFrame(reports_name, columns=['report_name'])
    output_df['patient_name'] = patient_names
    output_df['sx_dates'] = dates
    return output_df

reports_name_chemo = read_file_text(folder_path, string = 'chemotherapy', str1 = 'mr', str2 = 'ms', str3 = '\d{2}/\d{2}/\d{4}')

# def read_file_text(folder_path, destination_path, string = 'chemotherapy'):
#     file_names = os.listdir(folder_path)
#     reports_name = []
#     for file_name in file_names:
#         file = open(folder_path + '\\' + file_name, 'r')
#         file_text = file.read()
#         file_text.lower()
#         # print(file_text)
#         source_path = os.path.join(folder_path, file_name)
#         if string in file_text:
#             print('string_is_there')
#             reports_name.append(file_name)
#             shutil.copy(source_path, destination_path)
#         else:
#             print('string_is_not_there')
#     output_df = pd.DataFrame(reports_name, columns=['report_name'])
#     return output_df

reports_name_chemo = read_file_text(folder_path, destination_path, string = 'chemotherapy')
# reports_name_chemo.to_excel('D:\\Shweta\\path_reports\\2021_07_06_chemotherapy_reports_names_sk.xlsx', index=False)

## nact

reports_name_nact = read_file_text(folder_path, string = 'nact')

##

reports_name_hormone_therapy = read_file_text(folder_path, string = 'hormone therapy')

##

reports_name_treatment = read_file_text(folder_path, string = 'treatment')

##

reports_name_fibrosis = read_file_text(folder_path, destination_path = 'D:\\Shweta\\path_reports\\2021_06_07_fibrosis_path_reports_sk', string = 'fibrosis')
reports_name_fibrosis.to_excel('D:\\Shweta\\path_reports\\2021_07_06_fibrosis_reports_names_sk.xlsx', index=False)
