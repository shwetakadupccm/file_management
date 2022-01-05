import numpy as np
import pandas as pd
import re
from fuzzywuzzy import process, fuzz

folder_path = 'D:/Shweta/email/attachments_from_jehangir/all_jehangir/renamed_pdf_with_type'
sx_list = pd.read_excel('D:/Shweta/Surgery/2021_09_31_surgery_list_master_sk.xlsx')
sx_list_jeh = sx_list[sx_list.hospital_name == 'Jehangir Hospital']
report_info_df = pd.read_excel('D:/Shweta/email/attachments_from_jehangir/all_jehangir/output_df/2021_10_26_jeh_sx_report_names_sk.xlsx')
patient_names_unique = report_info_df['patient_name'].unique()

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', ' ', str(name))
        name = name.lower()
        name = re.sub('_', '', name)
        cleaned_names.append(name)
    return cleaned_names

def match_jeh_sx_path_reports(sx_patient_list_df, report_info_df, sx_name_str = 'Name ',
                                     report_name_str = 'patient_name'):
    sx_patient_names = clean_names(sx_patient_list_df, sx_name_str)
    sx_report_patient_names = clean_names(report_info_df, report_name_str)
    matched_report_patient_names = []
    for index, patient_name in enumerate(sx_patient_names):
        matched_name = process.extractOne(patient_name, sx_report_patient_names, scorer=fuzz.token_sort_ratio, score_cutoff=50)
        if matched_name is not None:
            print(matched_name)
            sx_df_cols = ['File_number', 'Sx Date', 'hospital_name']
            sx_df_dat = sx_patient_list_df.iloc[index][sx_df_cols]
            matched_name_index = sx_report_patient_names.index(matched_name[0])
            matched_report_patient_name = sx_report_patient_names[matched_name_index]
            score = matched_name[1]
            lst = [patient_name, matched_report_patient_name, score]
            final_lst = np.append(lst, sx_df_dat)
            matched_report_patient_names.append(final_lst)
    output_df = pd.DataFrame(matched_report_patient_names, columns=['patient_name_from_sx_list', 'matched_report_patient_name',
                                                                    'score', 'file_number', 'surgery_date', 'hospital_name'])
    return output_df

output_df = match_jeh_sx_path_reports(sx_list_jeh, report_info_df, sx_name_str = 'Name ',
                                     report_name_str = 'patient_name')

output_df.to_excel('D:/Shweta/email/attachments_from_jehangir/all_jehangir/sx_path_reports_matched_df/2021_11_02_sx_jeh_report_names_matching_with_all_cols.xlsx',
                   index=False)

