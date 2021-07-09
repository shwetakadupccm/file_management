import os
import pandas as pd
import numpy as np
import shutil
import re
from fuzzywuzzy import fuzz, process
import datetime

folder_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt'

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


def get_patient_name_from_report(report_text_lst, file_name):
    cleaned_file_name = re.sub("[\(\[].*?[\)\]]", "", file_name)
    cleaned_file_name = re.sub('.txt', '', cleaned_file_name)
    cleaned_file_name = re.sub('_', ' ', cleaned_file_name)
    patient_name = process.extractOne(cleaned_file_name, report_text_lst, scorer=fuzz.token_set_ratio, score_cutoff=100)
    if patient_name is not None:
        return cleaned_file_name

def get_tagged_date(report_text_lst, tag_str = 'sc date'):
    sc_date_name_index = report_text_lst.index(tag_str)
    sc_date_txt = report_text_lst[sc_date_name_index + 2]
    if sc_date_name_index is not None:
        match = re.search('\d{2}/\d{2}/\d{4}', sc_date_txt)
        date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
        if date is not None:
            return date

def get_keyword_info(file, string = 'chemotherapy'):
    pattern = re.compile(string, re.IGNORECASE)
    keyword_info = []
    for line in file:
        if pattern.search(line) != None:
            keyword_info.append(line.rstrip('\n'))
    return keyword_info

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


output_df = read_file_info_from_report(folder_path, date_str = 'sc date', keyword1 = 'chemotherapy', keyword2 = ['recur', 'Recur', 'ovar'])