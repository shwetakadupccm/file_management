import re
import pandas as pd
import os

pdf_folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy'
txt_files_folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_img_txt_files'

##
def get_report_text_into_list(file_path):
    file = open(file_path, 'rt')
    lines = []
    for line in file:
        line_txt = line.strip(':, \n')
        if line_txt.isdigit():
            lines.append(line_txt)
        else:
            line_txt_cleaned = line_txt.lower()
            line_txt_cleaned = re.sub('reference:dr.koppikercb ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.koppikercb', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('koppiker', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('sample collected at', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('orchids speciality breast care centre', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('flat no 1&2,', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('kapilvastu', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('sb road', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('next to ratna hospital', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('pune 411016 zone shiva', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('shva', '', line_txt_cleaned)
            lines.append(line_txt_cleaned)
    file.close()
    return lines

def get_unique_value_from_list(list_with_duplicate_values):
    unique_list = []
    for value in list_with_duplicate_values:
        if value not in unique_list:
            unique_list.append(value)
    return unique_list

text_lst = get_report_text_into_list(os.path.join(txt_files_folder_path, '06_20_bx_0.jpg.txt'))
text_df = pd.DataFrame(text_lst)
unique_text_lst = get_unique_value_from_list(text_lst)
unique_text_df = pd.DataFrame(unique_text_lst)

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
    try:
        specimen_index = text_lst.index(specimen_keyword)
        specimen_info = text_lst[specimen_index + 2]
        return specimen_info
    except ValueError:
        return None

def get_diagnosis(text_lst, diagnosis_keyword = 'diagnosis'):
    try:
        dia_index = text_lst.index(diagnosis_keyword)
        dia_info0 = text_lst[dia_index]
        dia_info1 = text_lst[dia_index - 1]
        dia_info2 = text_lst[dia_index + 1]
        dia_info3 = text_lst[dia_index + 2]
        dia_info = dia_info0 + ';' + dia_info1 + ';' + dia_info2 + ';' + dia_info3
        return dia_info
    except ValueError:
        return None

def get_report_info_from_txt_for_page_0(txt_files_folder_path, sid_keyword = 'sid', bx_dt_keyword = 'sample date', age_str = 'years',
                             gender_str = 'sex', specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis'):
    txt_files = os.listdir(txt_files_folder_path)
    file_names = []
    patient_names = []
    sids = []
    bx_dates = []
    ages = []
    genders = []
    specimens = []
    diagnosis_lst = []
    for txt_file in txt_files:
        if txt_file.endswith('0.txt'):
            print(txt_file)
            file_path = os.path.join(txt_files_folder_path, txt_file)
            file_text_lst = get_report_text_into_list(file_path)
            file_names.append(txt_file)
            patient_name = get_patient_name(file_text_lst)
            patient_names.append(patient_name)
            sid = get_sid(file_text_lst, sid_keyword)
            sids.append(sid)
            bx_date = get_biopsy_date(file_text_lst, bx_dt_keyword)
            bx_dates.append(bx_date)
            age = get_age(file_text_lst, age_str)
            ages.append(age)
            gender = get_gender(file_text_lst, gender_str)
            genders.append(gender)
            specimen = get_specimen(file_text_lst, specimen_keyword)
            specimens.append(specimen)
            diagnosis = get_diagnosis(file_text_lst, diagnosis_keyword)
            diagnosis_lst.append(diagnosis)
            print('done')
    output_df = pd.DataFrame(file_names, columns=['report_name'])
    output_df['patient_name'] = patient_names
    output_df['lab_sid'] = sids
    output_df['biopsy_date'] = bx_dates
    output_df['age'] = ages
    output_df['gender'] = genders
    output_df['specimen'] = specimens
    output_df['diagnosis'] = diagnosis_lst
    return output_df

df = get_report_info_from_txt_for_page_0(output_folder_path, sid_keyword = 'sid', bx_dt_keyword = 'sample date', age_str = 'years',
                             gender_str = 'sex', specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis')

df.to_excel('D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy\\bx_txt_files\\output_df\\2021_08_18_bx_path_page0_sk.xlsx',
            index=False)

###

def classify_report_by_type(text_lst, cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum']):
    report_type = []
    text_lst_str = str(text_lst)
    if cytology_keyword in text_lst_str:
        report_type.append('cytology')
    elif histology_keyword in text_lst_str:
        report_type.append('histology')
    elif ihc_keyword in text_lst_str:
        report_type.append('immunohistochemistry')
    elif blood_count_keyword in text_lst_str:
        report_type.append('complete_blood_count')
    elif ki_keyword in text_lst_str:
        report_type.append('ki67')
    elif glucose_keyword in text_lst_str:
        report_type.append('plasma_glucose')
    elif any(x in text_lst_str for x in nutrient_keyword):
        report_type.append('nutrient_report')
    elif liver_keyword in text_lst_str:
        report_type.append('liver_function_test')
    else:
        report_type.append('type_not_found')
    return report_type

def get_report_name_sid(txt_folder_path, sid_keyword = 'sid', cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin','calcium', 'phosphorus', 'urea', 'serum']):
    file_names = os.listdir(txt_folder_path)
    report_names = []
    report_types = []
    sids = []
    for file_name in file_names:
        if file_name.endswith('.txt'):
            report_names.append(file_name)
            file_txt = get_report_text_into_list(os.path.join(txt_folder_path, file_name))
            file_txt_unique = get_unique_value_from_list(file_txt)
            sid = get_sid(file_txt_unique, sid_keyword)
            sids.append(sid)
            report_type = classify_report_by_type(file_txt_unique, cytology_keyword, histology_keyword, ihc_keyword,
                                                 blood_count_keyword,
                                                  ki_keyword, glucose_keyword, liver_keyword,
                                                  nutrient_keyword
                                                  )
            report_types.append('; '.join([str(info) for info in report_type]))
    output_df = pd.DataFrame(report_names, columns=['report_name'])
    output_df['report_type'] = report_types
    output_df['lab_sid'] = sids
    return output_df

output_df = get_report_name_sid(txt_files_folder_path, sid_keyword = 'sid', cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin','calcium', 'phosphorus', 'urea', 'serum'])

output_df.to_excel('D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy\\bx_txt_files\\output_df\\2021_08_19_bx_path_report_type_sid_sk.xlsx',
            index=False)

