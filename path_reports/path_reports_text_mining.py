import os
import pandas as pd
import numpy as np
import re
from fuzzywuzzy import fuzz, process
import datetime

folder_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt'
file_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt\\Miss_LATA_MOHITE_-_H.txt'

def get_report_text_into_list(file_path):
    file = open(file_path, 'rt')
    lines = []
    for line in file:
        line_txt = line.strip(':, \n')
        if line_txt.isdigit():
            lines.append(line_txt)
        else:
            line_txt_cleaned = line_txt.lower()
            lines.append(line_txt_cleaned)
    file.close()
    return lines

report_text = get_report_text_into_list(file_path)

def get_patient_name_from_report(report_text_list, file_name):
    cleaned_file_name = re.sub("[\(\[].*?[\)\]]", "", file_name)
    cleaned_file_name = cleaned_file_name.lower()
    cleaned_file_name = re.sub('.txt', '', cleaned_file_name)
    cleaned_file_name = re.sub('miss.', '', cleaned_file_name)
    cleaned_file_name = re.sub('ms.', '', cleaned_file_name)
    cleaned_file_name = re.sub('mrs.', '', cleaned_file_name)
    cleaned_file_name = re.sub('mr.', '', cleaned_file_name)
    cleaned_file_name = re.sub('histo', '', cleaned_file_name)
    cleaned_file_name = re.sub('report', '', cleaned_file_name)
    cleaned_file_name = re.sub('_', ' ', cleaned_file_name)
    cleaned_file_name = re.sub(r'[0-9]', '', cleaned_file_name)
    cleaned_file_name = cleaned_file_name.split('-', 1)
    patient_name = process.extractOne(cleaned_file_name[0], report_text_list,
                                      scorer=fuzz.token_set_ratio, score_cutoff=100)
    if patient_name is not None:
        return cleaned_file_name[0]

def get_tagged_date(report_text_lst, tag_str = 'sc date'):
    try:
        sc_date_name_index = report_text_lst.index(tag_str)
        sc_date_txt = report_text_lst[sc_date_name_index + 2]
    except ValueError:
        return None
    if sc_date_name_index is not None:
        match = re.search('\d{2}/\d{2}/\d{4}', sc_date_txt)
        date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
        if date is not None:
            return date

date = get_tagged_date(report_text, tag_str='sc date')

def get_keyword_info(file_path, keyword = 'chemotherapy'):
    file = open(file_path, 'rt')
    pattern = re.compile(keyword, re.IGNORECASE)
    keyword_info = []
    for line in file:
        if pattern.search(line) != None:
            keyword_info.append(line.rstrip('\n'))
    file.close()
    return keyword_info

# keyword_info = get_keyword_info(file_path, keyword='chemotherapy')
# keyword_info2 = get_keyword_info(file_path, keyword = 'recur')
# keyword2 = ['recur', 'Recur', 'ovar']

def read_file_info_from_report(folder_path, date_str = 'sc date', keyword1 = 'chemotherapy', keyword2 = ['recur', 'ovar']):
    file_names = os.listdir(folder_path)
    identification_information = []
    report_name_1 = []
    keyword_1 = []
    keyword_info_1 = []
    keyword_2 = []
    keyword_info_2 = []

    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        file_text_lst = get_report_text_into_list(file_path)
        patient_name = get_patient_name_from_report(file_text_lst, file_name)
        sx_date = get_tagged_date(file_text_lst, date_str)
        indentification_info = np.append(patient_name, sx_date)
        identification_information.append(indentification_info)
        keyword_info1 = get_keyword_info(file_path, keyword1)
        if len(keyword_info1) != 0:
            keyword_info_1.append('; '.join([str(info) for info in keyword_info1]))
            keyword_1.append(keyword1)
            report_name_1.append(file_name)
        else:
            keyword_info_1.append('no_information_found')
            keyword_1.append('keyword_not_found')
            report_name_1.append('not_applicable')
        keyword_info_for_substring = []
        keyword_names = []
        for x in keyword2:
            keyword_info = get_keyword_info(file_path, x)
            if keyword_info is not None:
                keyword_info_for_substring.append('; '.join([str(info) for info in keyword_info]))
                keyword_names.append(x)
            else:
                keyword_info_for_substring.append('no_information_found')
                keyword_names.append('keyword_not_found')
        keyword_info_2.append(keyword_info_for_substring)
        keyword_2.append('; '.join([str(name) for name in keyword_names]))
    output_df = pd.DataFrame(identification_information, columns=['patient_name', 'sc_date'])
    output_df['report_name'] = report_name_1
    output_df['keyword_1'] = keyword_1
    output_df['key_word_info_1'] = keyword_info_1
    output_df['keyword_2'] = keyword_2
    output_df['key_word_info_2'] = keyword_info_2
    return output_df

output_df = read_file_info_from_report(folder_path, date_str = 'sc date', keyword1 = 'chemotherapy', keyword2 = ['recur', 'ovar'])
output_df.to_excel('D:\\Shweta\\path_reports\\2021_28_07_chemo_recu_info_sk.xlsx', index=False)

output_df1 = read_file_info_from_report(folder_path, date_str = 'sc date', keyword1 = 'tils', keyword2 = ['residual cancer burden'])
output_df1.to_excel('D:\\Shweta\\path_reports\\2021_28_07_tumour_tils_residual_cancer_info_1_sk.xlsx', index=False)

