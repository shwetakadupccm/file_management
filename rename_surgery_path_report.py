import os
import re
import pandas as pd
from fuzzywuzzy import fuzz, process

def clean_path_report_names(path):
    path_reports = os.listdir(path)
    cleaned_path_report_names = []
    for path_report in path_reports:
        cleaned_path_report = re.sub('[^a-zA-Z_0-9]', '_', path_report)
        cleaned_path_report = cleaned_path_report.lower()
        cleaned_path_report = cleaned_path_report.split('_')
        cleaned_path_report = '_'.join(cleaned_path_report)
        cleaned_path_report = cleaned_path_report.replace("__", "_")
        cleaned_path_report = cleaned_path_report.replace("___", "_")
        cleaned_path_report = cleaned_path_report.replace("_pdf", '.pdf')
        source = os.path.join(path, path_report)
        destination = os.path.join(path, cleaned_path_report)
        os.rename(source, destination)
        cleaned_path_report_names.append(cleaned_path_report)
    return cleaned_path_report_names

clean_path_report_names('D:\\Shweta\\Surgery\\Jehangir_Surgery_Path_Reports\\')

## get_nact_patients_path_reports

nact_patients = pd.read_excel('D:/Shweta/nact_data/nact_patients/nact_patient_list_for_path_data.xlsx')

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', ' ', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names

def match_nact_patient_report_and_copy(folder_path, df, name_str = 'patient_name'):
    cleaned_names = clean_names(df, name_str)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_name = re.sub(r'[^a-z_]', '', str(file))
            file_name = re.sub('___', '', file_name)
            file_name = re.sub('pdf', '', file_name)
            print(file_name)
            matched_name = process.extractOne(query=file_name, choices=cleaned_names,
                                              scorer=fuzz.token_set_ratio)
            print(matched_name)
            # file_path = os.path.join(root, file)

match_nact_patient_report_and_copy('Z:/Clinical_Database/Digitized_Files/Histopath/all_Jehangir_reports_year_wise', nact_patients,
                                   'patient_name')
