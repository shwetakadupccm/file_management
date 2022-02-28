import os
import pandas as pd
import numpy as np
import re
from fuzzywuzzy import fuzz, process
import datetime

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

def get_keyword_info(file_path, keyword = 'chemotherapy'):
    file = open(file_path, 'rt')
    pattern = re.compile(keyword, re.IGNORECASE)
    keyword_info = []
    for line in file:
        if pattern.search(line) != None:
            keyword_info.append(line.rstrip('\n'))
    file.close()
    return keyword_info

def get_class(keyword_info):
    keyword_info = str(keyword_info)
    keyword_info = keyword_info.lower()
    split_values = re.split('class', keyword_info)
    class_val = split_values[1]
    cleaned_value = re.sub('[^A-Za-z]+', '', class_val)
    class_value = re.sub('index', '', cleaned_value)
    class_value = class_value.upper()
    return class_value

# til = 'Tumour infiltrating lymphocytes are <5% class = III index = 0.215'
# class_val = get_class(til)

def get_tils_with_logical_sign(keyword_info, logical_operators = ['<','>']):
    if (any(log_operator in keyword_info for log_operator in logical_operators)):
        specific_number = re.sub(r'([^<|>0-9%])', '', str(keyword_info))
        return specific_number
    else:
        specific_number = re.sub(r'([^0-9%])', '', str(keyword_info))
        return specific_number

# til = 'Tumour infiltrating lymphocytes are <5%'
# til_score = get_tils_with_logical_sign(til, logical_operators = ['<', '>'])

def read_file_info_from_report(folder_path, date_str='sc date', keyword1='index', keyword2='class',
                               keyword3=['tumour', 'tils'], logical_operators=['<', '>']):
    file_names = os.listdir(folder_path)
    identification_information = []
    report_name_1 = []
    keyword_1 = []
    keyword_info_1 = []
    keyword_specific_numbers_1 = []
    keyword_2 = []
    keyword_info_2 = []
    keyword_specific_numbers_2 = []
    keyword_3 = []
    keyword_info_3 = []
    keyword_specific_numbers_3 = []
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        file_text_lst = get_report_text_into_list(file_path)
        patient_name = get_patient_name_from_report(file_text_lst, file_name)
        sx_date = get_tagged_date(file_text_lst, date_str)
        indentification_info = np.append(patient_name, sx_date)
        identification_information.append(indentification_info)
        report_name_1.append(file_name)
        keyword_info1 = get_keyword_info(file_path, keyword1)
        if len(keyword_info1) != 0:
            keyword_info_1.append('; '.join([str(info) for info in keyword_info1]))
            specific_number = re.findall('\d+\.\d+', str(keyword_info1))
            keyword_specific_numbers_1.append(' '.join([str(info) for info in specific_number]))
            keyword_1.append(keyword1)
        else:
            keyword_info_1.append('no_information_found')
            keyword_1.append('keyword_not_found')
            keyword_specific_numbers_1.append('not_found')
        keyword_info2 = get_keyword_info(file_path, keyword2)
        print(keyword_info2)
        if len(keyword_info2) != 0:
            keyword_info_2.append('; '.join([str(info) for info in keyword_info2]))
            keyword_2.append(keyword2)
            class_value = get_class(keyword_info2)
            keyword_specific_numbers_2.append(class_value)
        else:
            keyword_info_2.append('no_information_found')
            keyword_2.append('keyword_not_found')
            keyword_specific_numbers_2.append('not_found')
        keyword_info_for_substring = []
        keyword_names = []
        keyword_specific_numbers3 = []
        for x in keyword3:
            keyword_info3 = get_keyword_info(file_path, x)
            if keyword_info3 is not None:
                keyword_info_for_substring.append('; '.join([str(info) for info in keyword_info3]))
                specific_number = get_tils_with_logical_sign(keyword_info3, logical_operators)
                print(specific_number)
                keyword_specific_numbers3.append(specific_number)
                keyword_names.append(x)
            else:
                keyword_info_for_substring.append('no_information_found')
                keyword_names.append('keyword_not_found')
                keyword_specific_numbers_3.append('not_found')
        keyword_info_3.append(' '.join([str(info) for info in keyword_info_for_substring]))
        keyword_3.append('; '.join([str(name) for name in keyword_names]))
        keyword_specific_numbers_3.append(' '.join([no for no in keyword_specific_numbers3]))
    output_df = pd.DataFrame(identification_information, columns=['patient_name', 'sc_date'])
    output_df['report_name'] = report_name_1
    output_df['keyword_1'] = keyword_1
    output_df['key_word_info_1'] = keyword_info_1
    output_df['keyword_specific_numbers_1'] = keyword_specific_numbers_1
    output_df['keyword_2'] = keyword_2
    output_df['key_word_info_2'] = keyword_info_2
    output_df['keyword_specific_numbers_2'] = keyword_specific_numbers_2
    output_df['keyword_3'] = keyword_3
    output_df['key_word_info_3'] = keyword_info_3
    output_df['keyword_specific_numbers_3'] = keyword_specific_numbers_3
    return output_df

##
folder_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt'

output_df = read_file_info_from_report(folder_path, date_str = 'sc date', keyword1 = 'index', keyword2 = 'class',
                keyword3 = ['tumour infiltrating lymphocytes', 'tils'], logical_operators = ['<', '>'])

output_df.to_excel('D:\\Shweta\\path_reports\\2021_02_08_tils_class_index_sk.xlsx', index=False)

# def read_file_info_from_report(folder_path, date_str = 'sc date', keyword1 = 'tils', keyword2 = 'class', keyword3 = 'index'):
#     file_names = os.listdir(folder_path)
#     identification_information = []
#     report_name_1 = []
#     keyword_1 = []
#     keyword_info_1 = []
#     keyword_specific_numbers_1 = []
#     keyword_2 = []
#     keyword_info_2 = []
#     keyword_specific_numbers_2 = []
#     keyword_3 = []
#     keyword_info_3 = []
#     keyword_specific_numbers_3 = []
#
#     for file_name in file_names:
#         file_path = os.path.join(folder_path, file_name)
#         file_text_lst = get_report_text_into_list(file_path)
#         patient_name = get_patient_name_from_report(file_text_lst, file_name)
#         sx_date = get_tagged_date(file_text_lst, date_str)
#         indentification_info = np.append(patient_name, sx_date)
#         identification_information.append(indentification_info)
#         keyword_info1 = get_keyword_info(file_path, keyword1)
#         if len(keyword_info1) != 0:
#             keyword_info_1.append('; '.join([str(info) for info in keyword_info1]))
#             specific_number = re.sub(r'([^0-9%])', '', str(keyword_info1))
#             keyword_specific_numbers_1.append(specific_number)
#             keyword_1.append(keyword1)
#             report_name_1.append(file_name)
#         else:
#             keyword_info_1.append('no_information_found')
#             keyword_1.append('keyword_not_found')
#             keyword_specific_numbers_1.append('not_found')
#             report_name_1.append('not_applicable')
#         # keyword_info_for_substring = []
#         # keyword_names = []
#         keyword_info2 = get_keyword_info(file_path, keyword2)
#         print(keyword_info2)
#         if len(keyword_info2) != 0:
#             keyword_info_2.append('; '.join([str(info) for info in keyword_info2]))
#             keyword_2.append(keyword2)
#             keyword_info2 = str(keyword_info2)
#             keyword_info2 = keyword_info2.lower()
#             split_values = re.split('class', keyword_info2)
#             class_val = split_values[1]
#             cleaned_value = re.sub('[^A-Za-z]+', '', class_val)
#             class_value = re.sub('index', '', cleaned_value)
#             class_value = class_value.upper()
#             keyword_specific_numbers_2.append(class_value)
#         else:
#             keyword_info_2.append('no_information_found')
#             keyword_2.append('keyword_not_found')
#             keyword_specific_numbers_2.append('not_found')
#         keyword_info3 = get_keyword_info(file_path, keyword3)
#         print(keyword_info3)
#         if len(keyword_info3) != 0:
#             keyword_info_3.append('; '.join([str(info) for info in keyword_info3]))
#             keyword_3.append(keyword3)
#             keyword_specific_number3 = re.findall('\d+\.\d+', str(keyword_info3))
#             try:
#                 keyword_specific_numbers_3.append(keyword_specific_number3[0])
#             except IndexError:
#                 keyword_specific_numbers_3.append('None')
#         else:
#             keyword_info_3.append('no_information_found')
#             keyword_3.append('keyword_not_found')
#             keyword_specific_numbers_3.append('not_found')
#     output_df = pd.DataFrame(identification_information, columns=['patient_name', 'sc_date'])
#     output_df['report_name'] = report_name_1
#     output_df['keyword_1'] = keyword_1
#     output_df['key_word_info_1'] = keyword_info_1
#     output_df['keyword_1_specific_number'] = keyword_specific_numbers_1
#     output_df['keyword_2'] = keyword_2
#     output_df['key_word_info_2'] = keyword_info_2
#     output_df['keyword_2_specific_number'] = keyword_specific_numbers_2
#     output_df['keyword_3'] = keyword_3
#     output_df['key_word_info_3'] = keyword_info_3
#     output_df['keyword_3_specific_number'] = keyword_specific_numbers_3
#     return output_df
