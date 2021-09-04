import re
import pandas as pd
import os
import shutil
from fuzzywuzzy import fuzz, process

patient_names_df = pd.read_excel('D:/Shweta/nact_data/2021_02_17_NACT_final_dk.xlsx')

path_reports = os.listdir('D:/Shweta/path_reports/Jehangir_Surgery_Path_Reports')

def clean_report_name(folder_path):
    path_reports = os.listdir(folder_path)
    cleaned_report_name_lst = []
    for report in path_reports:
        cleaned_report_name = re.sub(r'[^a-zA-Z]', ' ', str(report))
        cleaned_report_name = cleaned_report_name.lower()
        cleaned_report_name = re.sub('pdf', '', cleaned_report_name)
        cleaned_report_name = re.sub('histo', '', cleaned_report_name)
        cleaned_report_name = re.sub('frozen', '', cleaned_report_name)
        cleaned_report_name = re.sub('radical', '', cleaned_report_name)
        cleaned_report_name = re.sub('redical', '', cleaned_report_name)
        cleaned_report_name = re.sub('ihc', '', cleaned_report_name)
        cleaned_report_name = re.sub('report', '', cleaned_report_name)
        cleaned_report_name = re.sub('review', '', cleaned_report_name)
        cleaned_report_name = re.sub('ms', '', cleaned_report_name)
        cleaned_report_name = re.sub('mrs', '', cleaned_report_name)
        cleaned_report_name_lst.append(cleaned_report_name)
    return cleaned_report_name_lst

clean_report_name('D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports')

def match_copy_nact_patients_reports(patient_list_df, source_path, destination_path):
    path_reports = os.listdir(source_path)
    path_reports_cleaned = clean_report_name(source_path)
    for patient_name in patient_list_df['patient_name']:
        patient_name = patient_name.lower()
        print(patient_name)
        match_name = process.extractOne(patient_name, path_reports_cleaned, scorer=fuzz.token_sort_ratio)
        print(match_name)
        matched_name_index = path_reports_cleaned.index(match_name[0])
        print(matched_name_index)
        matched_name_report_name = path_reports[matched_name_index]
        print(matched_name_report_name)
        file_source_path = os.path.join(source_path, matched_name_report_name)
        destination_path = os.path.join(destination_path)
        shutil.copy(file_source_path, destination_path)
        print('done')

# match_copy_nact_patients_reports(patient_names_df, 'D:/Shweta/path_reports/Jehangir_Surgery_Path_Reports',
#                                  'D:/Shweta/path_reports/2021_08_30_nact_path_reports')


