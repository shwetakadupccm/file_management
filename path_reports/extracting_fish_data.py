import os
import pandas as pd
import re
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
            line_txt_cleaned = re.sub('patient named', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('damage', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('specimen belongs', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('destruction of specimen', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('specimen shows', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('specimen using', '', line_txt_cleaned)
            lines.append(line_txt_cleaned)
    file.close()
    return lines

def get_unique_value_from_list(list_with_duplicate_values):
    unique_list = []
    for value in list_with_duplicate_values:
        if value not in unique_list:
            unique_list.append(value)
    output_lst = [line for line in unique_list if line]
    return output_lst

text = get_report_text_into_list(os.path.join('D:/Shweta/email/fish_reports/from_core_diagnostics/img_txt',
                                              'anju_shankar_peswani_19074762_pdl-1sp263ventana_report_0.txt'))
unique_txt = get_unique_value_from_list(text)
df = pd.DataFrame(unique_txt)

## core diagnostics

def get_patinet_name(report_text_lst, name_str = 'patient name'):
    for line in report_text_lst:
        if name_str in line:
            patient_name = re.sub('[^A-Za-z ]', '', str(line))
            patient_name = re.sub('patient', '', patient_name)
            patient_name = re.sub('name', '', patient_name)
            patient_name = re.sub('co re diag n o stic ss', '', patient_name)
            patient_name = re.sub('core diagnostic', '', patient_name)
            patient_name = patient_name.strip()
            return patient_name

patient_name = get_patinet_name(unique_txt, 'patient name')

def get_case_id(report_text_lst, case_id_keyword = 'case'):
    for line in report_text_lst:
        if case_id_keyword in line:
            case_id = re.sub('[^0-9]', '', str(line))
            return case_id

case_id = get_case_id(unique_txt, 'case id')

def get_age(text_lst, age_str = 'age'):
    for line in text_lst:
        if age_str in line:
            age = re.sub(r'[^0-9]', '', str(line))
            age = age[0:2]
            return age

age = get_age(unique_txt, 'age')

def get_gender(text_lst, gender_str = 'sex'):
    for line in text_lst:
        if gender_str in line:
            gender_txt = re.sub(r'[^a-zA-Z ]', '', str(line))
            cleaned_gender = re.sub('age', '', gender_txt)
            cleaned_gender = re.sub('yrs', '', cleaned_gender)
            cleaned_gender = re.sub('sex', '', cleaned_gender)
            spllited_txt = cleaned_gender.split()
            for value in spllited_txt:
                if value.endswith('ale'):
                    return value

gender = get_gender(unique_txt, 'sex')

def get_tagged_date(report_text_lst, tag_str = 'accessioning'):
    for line in report_text_lst:
        if tag_str in line:
            sc_date_name_index = report_text_lst.index(line)
            sc_date_txt = report_text_lst[sc_date_name_index]
            if sc_date_name_index is not None:
                try:
                    match = re.search('\d{2}/\d{2}/\d{4}', sc_date_txt)
                    date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
                    if date is not None:
                        return date
                except AttributeError:
                    return None

dt = get_tagged_date(unique_txt, 'accessioning')

def get_test_name(report_text_lst, test_name_str = 'test name'):
    for line in report_text_lst:
        if test_name_str in line:
            test_name_line_idx = report_text_lst.index(line)
            test_name = report_text_lst[test_name_line_idx + 1]
            return test_name

test_name = get_test_name(unique_txt, 'test name')

def get_specimen(report_txt_lst, specimen_keyword = 'specimen'):
    for line in report_txt_lst:
        if specimen_keyword in line:
            specimen_line_idx = report_txt_lst.index(line)
            specimen_0 = report_txt_lst[specimen_line_idx + 1]
            specimen_1 = report_txt_lst[specimen_line_idx + 2]
            specimen = specimen_0 + ' ' + specimen_1
            specimen = re.sub('clinical history', '', specimen)
            specimen = re.sub('cinical history', '', specimen)
            specimen = specimen.strip()
            return specimen

specimen = get_specimen(unique_txt, 'specimen')

def get_clinical_history(report_txt_lst, clinical_history_str = ['clinical history', 'cinical history']):
    for line in report_txt_lst:
        if any(x in line for x in clinical_history_str):
            clinical_history_line_idx = report_txt_lst.index(line)
            clinical_history = report_txt_lst[clinical_history_line_idx + 1]
            return clinical_history

clinical_history = get_clinical_history(unique_txt, 'clinical history')

def get_methodology(report_txt_lst, methodology_keyword = 'methodology'):
    for line in report_txt_lst:
        if methodology_keyword in line:
            methodology_line_idx = report_txt_lst.index(line)
            methodology = report_txt_lst[methodology_line_idx + 1]
            return methodology

methodology = get_methodology(unique_txt, 'methodology')

def make_hyperlink(path, file_name):
    url = "{}"
    return '=HYPERLINK("%s", "%s")' % (url.format(path), file_name)

def get_jpg_file_path(folder_path, file):
    file_name = re.sub('.txt', '.jpg', file)
    file_path = os.path.join(folder_path, file_name)
    return file_name, file_path

def get_all_core_diagnostics_report_data(folder_path, name_str = 'patient name', age_str = 'age', gender_str = 'sex',
                                         case_id_keyword = 'case', tag_str = 'accessioning', test_name_str = 'test name',
                                         specimen_keyword = 'specimen', clinical_history_str = ['clinical history', 'cinical history'],
                                         methodology_keyword = 'methodology'):
    file_names = os.listdir(folder_path)
    data_lst = []
    for file_name in file_names:
        if file_name.endswith('.txt'):
            jpg_file_name, jpg_file_path = get_jpg_file_path(folder_path, file_name)
            hyperlink = make_hyperlink(jpg_file_path, jpg_file_name)
            file_txt = get_report_text_into_list(os.path.join(folder_path, file_name))
            unique_file_txt = get_unique_value_from_list(file_txt)
            patient_name = get_patinet_name(unique_file_txt, name_str)
            age = get_age(unique_file_txt, age_str)
            gender = get_gender(unique_file_txt, gender_str)
            case_id = get_case_id(unique_file_txt, case_id_keyword)
            sample_date = get_tagged_date(unique_file_txt, tag_str)
            test_name = get_test_name(unique_file_txt, test_name_str)
            specimen = get_specimen(unique_file_txt, specimen_keyword)
            clinical_history = get_clinical_history(unique_file_txt, clinical_history_str)
            methodology = get_methodology(unique_file_txt, methodology_keyword)
            lst = [file_name, hyperlink, patient_name, age, gender, case_id, sample_date, test_name, specimen, clinical_history,
                   methodology]
            data_lst.append(lst)
    df = pd.DataFrame(data_lst, columns=['file_name', 'hyperlink', 'patient_name', 'age', 'gender', 'case_id', 'sample_date',
                                    'test_name', 'specimen', 'clinical_history', 'methodology'])
    return df

data_df = get_all_core_diagnostics_report_data('D:/Shweta/email/fish_reports/from_core_diagnostics/img_txt', name_str = 'patient name',
        age_str = 'age', gender_str = 'sex', case_id_keyword = 'case', tag_str = 'accessioning',
        test_name_str = 'test name', specimen_keyword = 'specimen', clinical_history_str = ['clinical history', 'cinical history'],
        methodology_keyword = 'methodology')

data_df.to_excel('D:/Shweta/email/fish_reports/from_core_diagnostics/img_txt/output_df/2021_10_20_fish_test_extracted_core_sk.xlsx',
                 index = False)

## gene lab


