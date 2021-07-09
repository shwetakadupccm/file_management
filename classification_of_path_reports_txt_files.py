import os
import pandas as pd
import numpy as np
import shutil
import re
from fuzzywuzzy import fuzz, process
import datetime

folder_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt'

lines = []
file_name = 'BHAGWANTI_PANDYA_[_histo_large].txt'
file = open('D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt\\BHAGWANTI_PANDYA_[_histo_large].txt', 'rt')
file_text = file.read()

cleaned_file_name = re.sub("[\(\[].*?[\)\]]", "", file_name)
cleaned_file_name = re.sub('.txt', '', cleaned_file_name)
cleaned_file_name1 = re.sub('_', ' ', cleaned_file_name)

lines = []
for line in file:
    line_txt = line.strip(':, \n' )
    if line_txt.isdigit():
        lines.append(line_txt)
    else:
        line_txt_cleaned = line_txt.lower()
        lines.append(line_txt_cleaned)

def get_report_text_into_list(file):
    lines = []
    for line in file:
        line_txt = line.strip(':, \n')
        if line_txt.isdigit():
            lines.append(line_txt)
        else:
            line_txt_cleaned = line_txt.lower()
            lines.append(line_txt_cleaned)
    return lines

sc_date_index = lines.index('sc date')
sc_date = lines[sc_date_index + 2]
match = re.search('\d{2}/\d{2}/\d{4}', sc_date)
date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()

def get_tagged_date(report_text_lst, tag_str = 'sc date'):
    sc_date_name_index = report_text_lst.index(tag_str)
    sc_date_txt = report_text_lst[sc_date_name_index + 2]
    if sc_date_name_index is not None:
        match = re.search('\d{2}/\d{2}/\d{4}', sc_date_txt)
        date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
        if date is not None:
            return date

dt = get_tagged_date(lines, tag_str = 'sc date')
lines_df = pd.DataFrame(lines)
process.extractOne(cleaned_file_name1, lines, scorer=fuzz.token_set_ratio, score_cutoff=100)

def get_patient_name_from_report(report_text_lst, file_name):
    cleaned_file_name = re.sub("[\(\[].*?[\)\]]", "", file_name)
    cleaned_file_name = re.sub('.txt', '', cleaned_file_name)
    cleaned_file_name = re.sub('_', ' ', cleaned_file_name)
    patient_name = process.extractOne(cleaned_file_name, report_text_lst, scorer=fuzz.token_set_ratio, score_cutoff=100)
    if patient_name is not None:
        return cleaned_file_name

name = get_patient_name_from_report(lines, file_name)

def get_patient_name_key_word_info(file, str1 = 'ms', keyword = 'chemotherapy'):
    pattern1 = re.compile(str1, re.IGNORECASE)
    keyword_pattern = re.compile(keyword, re.IGNORECASE)
    patient_names = []
    dates = []
    keyword_info = []
    for line in file:
        if pattern1.search(line) != None:
            patient_names.append(line.rstrip('\n'))
        elif keyword_pattern.search(line) != None:
            keyword_info.append(line.rstrip('\n'))
    return keyword_info

key_word_info = get_patient_name_key_word_info(file, str1 = 'ms', keyword = 'chemotherapy')

string = 'chemotherapy'

def get_keyword_info(file, string = 'chemotherapy'):
    pattern = re.compile(string, re.IGNORECASE)
    keyword_info = []
    for line in file:
        if pattern.search(line) != None:
            keyword_info.append(line.rstrip('\n'))
    return keyword_info

keyword_info = get_keyword_info(file, string = 'chemotherapy')
##
def read_file_info_from_report(folder_path, keyword1 = 'chemotherapy', keyword2 = ['recur', 'Recur', 'ovar']):
    file_names = os.listdir(folder_path)
    report_name_1 = []
    keyword_1 = []
    keyword_info_1 = []
    report_name_2 = []
    keyword_2 = []

    for file_name in file_names:
        if file_name == 'search_terms.txt':
            continue
        file = open(folder_path + '\\' + file_name, 'rt')
        keyword_info1 = get_patient_name_key_word_info(file, keyword1)
        print(keyword_info1)
        if len(keyword_info1) != 0:
            keyword_info_1.append('; '.join([str(info) for info in keyword_info1]))
        else:
            keyword_info_1.append('no_information_found')
        file_r = open(folder_path + '\\' + file_name, 'r')
        file_text = file_r.read()
        if keyword1 in file_text:
            report_name_1.append(file_name)
            keyword_1.append(keyword1)
        else:
            print('string_is_not_there')
            report_name_1.append('not_applicable')
            keyword_1.append('not_found')
        if any(x in file_text for x in keyword2):
            report_name_2.append(file_name)
            keyword_2.append(keyword2)
        else:
            report_name_2.append('not_applicable')
            keyword_2.append('not_found')
    output_df = pd.DataFrame(report_name_1, columns = ['report_name'])
    output_df['keyword_1'] = keyword_1
    output_df['key_word_info'] = keyword_info_1
    output_df['report_name_other_than_key'] = report_name_2
    output_df['keyword_2'] = keyword_2
    return output_df

keyword_info_new = read_file_info_from_report(folder_path, keyword1 = 'chemotherapy', keyword2 = ['recur', 'Recur', 'ovar'])

folder_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt'
destination_path = 'D:\\Shweta\\path_reports\\2021_07_07_chemo_path_reports_sk'
pdf_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports'

def read_file_info_from_report(folder_path, date_str = 'sc date', keyword1 = 'chemotherapy', keyword2 = ['recur', 'Recur', 'ovar']):
    file_names = os.listdir(folder_path)
    identification_information = []
    report_name_1 = []
    keyword_1 = []
    keyword_info_1 = []
    report_name_2 = []
    keyword_2 = []
    keyword_info_2 = []

    for file_name in file_names:
        if file_name == 'search_terms.txt':
            continue
        file = open(folder_path + '\\' + file_name, 'rt')

        file_text_lst = get_report_text_into_list(file)
        patient_name = get_patient_name_from_report(file_text_lst, file_name)
        sx_date = get_tagged_date(file_text_lst, date_str)
        indentification_info = np.append(patient_name, sx_date)
        identification_information.append(indentification_info)
        file.close()
        keyword_info1 = get_keyword_info(file, keyword1)
        if len(keyword_info1) != 0:
            keyword_info_1.append('; '.join([str(info) for info in keyword_info1]))
        else:
            keyword_info_1.append('no_information_found')
        file_r = open(folder_path + '\\' + file_name, 'r')
        file_text = file_r.read()
        if keyword1 in file_text:
            report_name_1.append(file_name)
            keyword_1.append(keyword1)
        else:
            print('string_is_not_there')
            report_name_1.append('not_applicable')
            keyword_1.append('not_found')
        if any(x in file_text for x in keyword2):
            report_name_2.append(file_name)
            keyword_2.append(keyword2)
        else:
            report_name_2.append('not_applicable')
            keyword_2.append('not_found')
    output_df = pd.DataFrame(identification_information, columns=['patient_name', 'sc_date'])
    output_df['report_name'] = report_name_1
    output_df['keyword_1'] = keyword_1
    output_df['key_word_info'] = keyword_info_1
    output_df['report_name_other_than_key'] = report_name_2
    output_df['keyword_2'] = keyword_2
    return output_df

output_df = read_file_info_from_report(folder_path, keyword1 = 'chemotherapy', keyword2 = ['recur', 'Recur', 'ovar'], date_str = 'sc date')
# def read_file_text(folder_path, keyword1 = 'chemotherapy', keyword2 = ['recur', 'Recur', 'ovar'],  str1 = 'mr', str2 = 'mrs', str3 = 'miss', str4 = 'ms', str5 = '\d{2}/\d{2}/\d{4}'):
#     file_names = os.listdir(folder_path)
#     patient_names = []
#     dates = []
#     reports_name1 = []
#     keyword_1 = []
#     keyword_info1 = []
#     reports_name2 = []
#     keyword_2 = []
#     for file_name in file_names:
#         if file_name == 'search_terms.txt':
#             continue
#         file = open(folder_path + '\\' + file_name, 'rt')
#         patient_name, dts, keyword_info = get_patient_name_surgery_date(file, keyword1, str1, str2, str3, str4)
#         if len(patient_name) != 0:
#             patient_names.append(patient_name[0])
#         else:
#             patient_names.append('name_not_available')
#         dates.append(', '.join([str(dt) for dt in dts]))
#         if len(keyword_info) != 0:
#             keyword_info1.append(', '.join([str(info) for info in keyword_info]))
#         else:
#             keyword_info1.append('no_information_found')
#         file_r = open(folder_path + '\\' + file_name, 'r')
#         file_text = file_r.read()
#         file_text.lower()
#         # print(file_text)
#         if keyword1 in file_text:
#             reports_name1.append(file_name)
#             keyword_1.append(keyword1)
#             # keyword_info = get_keyword_info(file, string1)
#             # keyword_info1.append(', '.join([str(info) for info in keyword_info]))
#         else:
#             print('string_is_not_there')
#             reports_name1.append('not_applicable')
#             keyword_1.append('not_found')
#             # keyword_info1.append('no_information_found')
#         if any(x in file_text for x in keyword2):
#             reports_name2.append(file_name)
#             keyword_2.append(keyword2)
#         else:
#             reports_name2.append('not_applicable')
#             keyword_2.append('not_found')
#     output_df = pd.DataFrame(reports_name1, columns=['report_name'])
#     output_df['keyword_1'] = keyword_1
#     output_df['key_word_info'] = keyword_info1
#     output_df['report_name_other_than_key'] = reports_name2
#     output_df['keyword_2'] = keyword_2
#     output_df['patient_name'] = patient_names
#     output_df['sx_dates'] = dates
#     return output_df

def read_file_info_from_report(folder_path, date_str = 'sc date'):
    file_names = os.listdir(folder_path)
    identification_information = []
    keyword_info_lst = []
    for file_name in file_names:
        if file_name == 'search_terms.txt':
            continue
        file = open(folder_path + '\\' + file_name, 'rt')
        file_text_lst = get_report_text_into_list(file)
        patient_name = get_patient_name_from_report(file_text_lst, file_name)
        print(patient_name)
        sc_date = get_tagged_date(file_text_lst, date_str)
        print(sc_date)
        indentification_info = np.append(patient_name, sc_date)
        identification_information.append(indentification_info)
    output_df = pd.DataFrame(identification_information, columns=['patient_name', 'sc_date'])
    return output_df


output_df = read_file_info_from_report(folder_path, date_str = 'sc date')

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
