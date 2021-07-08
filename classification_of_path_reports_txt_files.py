import os
import pandas as pd
import shutil
import re

lines = []
file = open('D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt\\BHAGWANTI_PANDYA_[_histo_large].txt', 'rt')

def get_patient_name_surgery_date(file, keyword = 'chemotherapy', str1 = 'mr', str2 = 'mrs', str3 = 'miss', str4 = 'ms', str5 = '\d{2}/\d{2}/\d{4}'):
    pattern1 = re.compile(str1, re.IGNORECASE)
    pattern2 = re.compile(str2, re.IGNORECASE)
    pattern3 = re.compile(str3, re.IGNORECASE)
    pattern4 = re.compile(str4, re.IGNORECASE)
    pattern5 = re.compile(str5)
    keyword_pattern = re.compile(keyword, re.IGNORECASE)
    patient_names = []
    dates = []
    keyword_info = []
    for line in file:
        if pattern1.search(line) != None:
            patient_names.append(line.rstrip('\n'))
        elif pattern2.search(line) != None:
            patient_names.append(line.rstrip('\n'))
        elif pattern3.search(line) != None:
            patient_names.append(line.rstrip('\n'))
        elif pattern4.search(line) != None:
            patient_names.append(line.rstrip('\n'))
        elif pattern5.search(line) != None:
            date = line.rstrip('\n')
            cleaned_date = date.replace(':', '')
            final_date = cleaned_date[0:11]
            dates.append(final_date)
        elif keyword_pattern.search(line) != None:
            keyword_info.append(line.rstrip('\n'))
    return patient_names, dates, keyword_info

patient_names, dates = get_patient_name_surgery_date(file, str1 = 'mr', str2 = 'ms', str3 = '\d{2}/\d{2}/\d{4}')

string = 'chemotherapy'

def get_keyword_info(file, string1 = 'chemotherapy'):
    pattern = re.compile(string1, re.IGNORECASE)
    keyword_info = []
    for line in file:
        if pattern.search(line) != None:
            keyword_info.append(line.rstrip('\n'))
            # print(line)
    return keyword_info

keyword_info = get_keyword_info(file, string1 = 'chemotherapy')
##
folder_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt'
destination_path = 'D:\\Shweta\\path_reports\\2021_07_07_chemo_path_reports_sk'
pdf_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports'

def read_file_text(folder_path, keyword1 = 'chemotherapy', keyword2 = ['recur', 'Recur', 'ovar'],  str1 = 'mr', str2 = 'mrs', str3 = 'miss', str4 = 'ms', str5 = '\d{2}/\d{2}/\d{4}'):
    file_names = os.listdir(folder_path)
    patient_names = []
    dates = []
    reports_name1 = []
    keyword_1 = []
    keyword_info1 = []
    reports_name2 = []
    keyword_2 = []
    for file_name in file_names:
        if file_name == 'search_terms.txt':
            continue
        file = open(folder_path + '\\' + file_name, 'rt')
        patient_name, dts, keyword_info = get_patient_name_surgery_date(file, keyword1, str1, str2, str3, str4)
        if len(patient_name) != 0:
            patient_names.append(patient_name[0])
        else:
            patient_names.append('name_not_available')
        dates.append(', '.join([str(dt) for dt in dts]))
        if len(keyword_info) != 0:
            keyword_info1.append(', '.join([str(info) for info in keyword_info]))
        else:
            keyword_info1.append('no_information_found')
        file_r = open(folder_path + '\\' + file_name, 'r')
        file_text = file_r.read()
        file_text.lower()
        # print(file_text)
        if keyword1 in file_text:
            reports_name1.append(file_name)
            keyword_1.append(keyword1)
            # keyword_info = get_keyword_info(file, string1)
            # keyword_info1.append(', '.join([str(info) for info in keyword_info]))
        else:
            print('string_is_not_there')
            reports_name1.append('not_applicable')
            keyword_1.append('not_found')
            # keyword_info1.append('no_information_found')
        if any(x in file_text for x in keyword2):
            reports_name2.append(file_name)
            keyword_2.append(keyword2)
        else:
            reports_name2.append('not_applicable')
            keyword_2.append('not_found')
    output_df = pd.DataFrame(reports_name1, columns=['report_name'])
    output_df['keyword_1'] = keyword_1
    output_df['key_word_info'] = keyword_info1
    output_df['report_name_other_than_key'] = reports_name2
    output_df['keyword_2'] = keyword_2
    output_df['patient_name'] = patient_names
    output_df['sx_dates'] = dates
    return output_df

reports_name_chemo = read_file_text(folder_path, keyword1 = 'chemotherapy', keyword2 = ['recur','Recur', 'ovar'], str1 = 'mr', str2 = 'mrs', str3 = 'miss', str4 = 'ms', str5 = '\d{2}/\d{2}/\d{4}')
chemo_path_reports = reports_name_chemo.loc[reports_name_chemo['report_name'] != 'not_applicable']
chemo_path_reports.to_excel('D:\\Shweta\\path_reports\\2021_07_08_chemotherapy_with_keyword_info_sk.xlsx', index=False)


def read_file_text(folder_path, pdf_path, destination_path, string = 'chemotherapy'):
    file_names = os.listdir(folder_path)
    reports_name = []
    for file_name in file_names:
        if file_name == 'search_terms.txt':
            continue
        print(file_name)
        file = open(folder_path + '\\' + file_name, 'r')
        file_text = file.read()
        file_text.lower()
        # print(file_text)
        pdf_file_name = file_name.replace('.txt', '.pdf')
        source_path = os.path.join(pdf_path, pdf_file_name)
        if string in file_text:
            print('string_is_there')
            reports_name.append(file_name)
            shutil.copy(source_path, destination_path)
        else:
            print('string_is_not_there')
    output_df = pd.DataFrame(reports_name, columns=['report_name'])
    return output_df

reports_name_chemo = read_file_text(folder_path, pdf_path, destination_path, string = 'chemotherapy')

## nact

reports_name_nact = read_file_text(folder_path, string = 'nact')

##

reports_name_hormone_therapy = read_file_text(folder_path, string = 'hormone therapy')

##

reports_name_treatment = read_file_text(folder_path, string = 'treatment')

##

reports_name_fibrosis = read_file_text(folder_path, pdf_path, destination_path = 'D:\\Shweta\\path_reports\\2021_07_07_fibrosis_path_reports_sk', string = 'fibrosis')
reports_name_fibrosis.to_excel('D:\\Shweta\\path_reports\\2021_07_06_fibrosis_reports_names_sk.xlsx', index=False)
