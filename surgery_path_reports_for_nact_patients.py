import pandas as pd
import os
import shutil
from fuzzywuzzy import fuzz, process

patient_names_df = pd.read_excel('D:\\Shweta\\path_reports\\path_report_mining_output_checked_dk.xlsx')

path_reports = os.listdir('D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports')

for patient_name in patient_names_df['patient_name']:
    print(patient_name)
    match_name = process.extractOne(patient_name, path_reports, scorer=fuzz.token_sort_ratio)
    print(match_name)
    source_path = os.path.join('D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports', match_name[0])
    destination_path = os.path.join('D:\\Shweta\\path_reports\\2021_21_07_sx_reports_to_dr_nutan_sk', match_name[0])
    shutil.copy(source_path, destination_path)
    print('done')
