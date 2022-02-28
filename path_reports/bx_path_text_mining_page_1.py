import re
import pandas as pd
import os

folder_path = 'D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy'
txt_folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_txt_files'

##
def get_report_text_into_list(file_path):
    file = open(file_path, 'rt', encoding='utf-8')
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

def get_unique_value_from_list(list_with_duplicate_values):
    unique_list = []
    for value in list_with_duplicate_values:
        if value not in unique_list:
            unique_list.append(value)
    return unique_list

text_lst = get_report_text_into_list(os.path.join(txt_folder_path, '107_19_FNAC_Bx_page_1.txt'))
text_df = pd.DataFrame(text_lst)
unique_list = get_unique_value_from_list(text_lst)
unique_df = pd.DataFrame(unique_list)

def get_patient_name(text_lst):
    patient_name = text_lst[0]
    return patient_name

def get_sid(text_lst, sid_keyword = 'sid'):
    for line in text_lst:
        if sid_keyword in line:
            sid = re.sub('\D', '', str(line))
            return sid

def get_biopsy_date(text_lst, bx_dt_keyword = 'sample date'):
    try:
        bx_dt_index = text_lst.index(bx_dt_keyword)
        bx_dt = text_lst[bx_dt_index + 1]
        return bx_dt
    except ValueError:
        return None

def get_age(text_lst, age_str = 'years'):
    for line in text_lst:
        if age_str in line:
            print(line)
            age = re.sub(r'[^0-9]', '', str(line))
            age = age[0:2]
            return age

def get_gender(text_lst, gender_str = 'sex'):
    for line in text_lst:
        if gender_str in line:
            gender_txt = re.sub(r'[^a-zA-Z]', '', str(line))
            cleaned_gender = re.sub('age', '', gender_txt)
            cleaned_gender = re.sub('years', '', cleaned_gender)
            cleaned_gender = re.sub('sex', '', cleaned_gender)
            return cleaned_gender

def get_specimen(text_lst, specimen_keyword = 'specimen'):
    for line in text_lst:
        if specimen_keyword in line:
            return line

def get_diagnosis(text_lst, diagnosis_keyword = 'diagnosis'):
    for line in text_lst:
        if diagnosis_keyword in line:
            dia_index = text_lst.index(line)
            dia_info1 = text_lst[dia_index + 1]
            dia_info2 = text_lst[dia_index + 2]
            dia_info3 = text_lst[dia_index + 3]
            dia_info4 = text_lst[dia_index + 4]
            dia_info = dia_info1 + ';' + dia_info2 + ';' + dia_info3 + ';' + dia_info4
            return dia_info

dia = get_diagnosis(text_lst, diagnosis_keyword = 'diagnosis')

def get_notthingham_grade(text_lst, nottingham_keyword = 'nottingham'):
    for line in text_lst:
        if nottingham_keyword in line:
            notingham_grade = re.sub('modified nottingham’s histologic', '', line)
            notingham_grade = re.split(',', notingham_grade)
            notingham_grade = notingham_grade[0]
            return notingham_grade

not_score = get_notthingham_grade(unique_list, nottingham_keyword = 'nottingham')

def get_notthingham_score(text_lst, nottingham_score_keyword = 'nottingham'):
    for line in text_lst:
        if nottingham_score_keyword in line:
            notingham_score = re.sub('modified nottingham’s histologic', '', line)
            notingham_score = re.split(',', notingham_score)
            notingham_score = notingham_score[1]
            notingham_score = re.sub('score', '', notingham_score)
            notingham_score = re.sub(':', '', notingham_score)
            return notingham_score

not_score = get_notthingham_score(unique_list, nottingham_score_keyword = 'nottingham')

def get_report_info_from_txt_for_page_1(txt_files_folder_path, sid_keyword = 'sid', bx_dt_keyword = 'sample date', age_str = 'years',
                             gender_str = 'sex', specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis',
                                        nottingham_keyword = 'nottingham', nottingham_score_keyword = 'nottingham'):
    txt_files = os.listdir(txt_files_folder_path)
    file_names = []
    patient_names = []
    sids = []
    bx_dates = []
    ages = []
    genders = []
    specimens = []
    diagnosis_lst = []
    nottingham_grade_lst = []
    nottingham_score_lst = []
    for txt_file in txt_files:
        if txt_file.endswith('1.txt'):
            print(txt_file)
            file_path = os.path.join(txt_files_folder_path, txt_file)
            file_text_lst = get_report_text_into_list(file_path)
            file_text_lst_unique = get_unique_value_from_list(file_text_lst)
            file_names.append(txt_file)
            patient_name = get_patient_name(file_text_lst_unique)
            patient_names.append(patient_name)
            sid = get_sid(file_text_lst_unique, sid_keyword)
            sids.append(sid)
            bx_date = get_biopsy_date(file_text_lst_unique, bx_dt_keyword)
            bx_dates.append(bx_date)
            age = get_age(file_text_lst, age_str)
            ages.append(age)
            gender = get_gender(file_text_lst_unique, gender_str)
            genders.append(gender)
            specimen = get_specimen(file_text_lst_unique, specimen_keyword)
            specimens.append(specimen)
            diagnosis = get_diagnosis(file_text_lst_unique, diagnosis_keyword)
            diagnosis_lst.append(diagnosis)
            nottingham_grade = get_notthingham_grade(file_text_lst_unique, nottingham_keyword)
            nottingham_grade_lst.append(nottingham_grade)
            nottingham_score = get_notthingham_score(file_text_lst_unique, nottingham_score_keyword)
            nottingham_score_lst.append(nottingham_score)
            print('done')
    output_df = pd.DataFrame(file_names, columns=['report_name'])
    output_df['patient_name'] = patient_names
    output_df['lab_sid'] = sids
    output_df['biopsy_date'] = bx_dates
    output_df['age'] = ages
    output_df['gender'] = genders
    output_df['specimen'] = specimens
    output_df['diagnosis'] = diagnosis_lst
    output_df['nottingham_grade'] = nottingham_grade_lst
    output_df['nottingham_score'] = nottingham_score_lst
    return output_df

df = get_report_info_from_txt_for_page_1(txt_folder_path, sid_keyword = 'sid', bx_dt_keyword = 'sample date', age_str = 'years',
                             gender_str = 'sex', specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis',
                                         nottingham_keyword = 'nottingham', nottingham_score_keyword = 'nottingham')

df.to_excel('D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy\\bx_txt_files\\output_df\\2021_08_19_bx_path_page1_sk.xlsx',
            index=False)
