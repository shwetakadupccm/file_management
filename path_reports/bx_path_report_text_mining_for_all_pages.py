import re
import pandas as pd
import os
import datetime

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
            line_txt_cleaned = re.sub('reference', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.koppikercb', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('koppiker', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('sample collected at', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('orchids speciality breast care centre', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('flat no 1&2,', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('kapilvastu', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('sb road', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('next to ratna hospital', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('pune 411016 zone shiva', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('pune 411016zone shiva', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('pune 411016 zone', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('zone shiva', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('shva', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.c b ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.cb ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr. cb ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr. c b, ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('c b ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('deshmukh chetan d md', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.deshmukh chetan d mbd', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('accreditation asper iso certno mc refer scope wwwnablindiaorg', '', line_txt_cleaned)
            lines.append(line_txt_cleaned)
    file.close()
    return lines

def get_unique_value_from_list(list_with_duplicate_values):
    unique_list = []
    for value in list_with_duplicate_values:
        if value not in unique_list:
            unique_list.append(value)
    return unique_list

text_lst = get_report_text_into_list(os.path.join(txt_files_folder_path, '06_20_bx_2.jpg.txt'))
text_df = pd.DataFrame(text_lst)
unique_text_lst = get_unique_value_from_list(text_lst)
unique_text_df = pd.DataFrame(unique_text_lst)

def get_sid(text_lst, sid_keyword = 'sid'):
    for line in text_lst:
        if sid_keyword in line:
            sid = re.sub('\D', '', str(line))
            return sid

def get_patient_name(text_lst):
    patient_name = text_lst[0]
    cleaned_patient_name = re.sub(r'[^a-zA-Z ]', '', str(patient_name))
    cleaned_patient_name = re.sub('sid', '', cleaned_patient_name)
    if cleaned_patient_name is not None:
        return cleaned_patient_name

def get_sample_date(text_lst, sample_dt_keyword = 'sample date'):
    for line in text_lst:
        if sample_dt_keyword in line:
            sample_dt_index = text_lst.index(line)
            sample_dt = text_lst[sample_dt_index + 1]
            match = re.search('\d{2}-\d{2}-\d{4}', sample_dt)
            if match is not None:
                date = datetime.datetime.strptime(match.group(), '%d-%m-%Y').date()
                return date

date = get_sample_date(unique_text_lst, 'sample date')

def get_age(text_lst, age_str = 'years'):
    for line in text_lst:
        if age_str in line:
            cleaned_line = re.sub('\d{2}-\d{2}-\d{4}', '', line)
            cleaned_line = re.sub('\d{2}:\d{2}', '', cleaned_line)
            age = re.sub(r'[^0-9]', '', str(cleaned_line))
            age = age[0:2]
            return age

def get_gender(text_lst, gender_str = 'sex'):
    for line in text_lst:
        if gender_str in line:
            gender_txt = re.sub(r'[^a-zA-Z]', '', str(line))
            cleaned_gender = re.sub('age', '', gender_txt)
            cleaned_gender = re.sub('years', '', cleaned_gender)
            cleaned_gender = re.sub('sex', '', cleaned_gender)
            cleaned_gender = re.sub('am', '', cleaned_gender)
            cleaned_gender = re.sub('pm', '', cleaned_gender)
            return cleaned_gender

def get_specimen(text_lst, specimen_keyword = 'specimen'):
    for line in text_lst:
        if specimen_keyword in line:
            return line

def get_diagnosis(text_lst, diagnosis_keyword = 'diagnosis'):
    for line in text_lst:
        if diagnosis_keyword in line:
            dia_index = text_lst.index(line)
            dia_info0 = text_lst[dia_index]
            dia_info1 = text_lst[dia_index - 1]
            dia_info2 = text_lst[dia_index + 1]
            dia_info3 = text_lst[dia_index + 2]
            dia_info = dia_info0 + ' ; ' + dia_info1 + ' ; ' + dia_info2 + ' ; ' + dia_info3
            return dia_info

def get_notthingham_grade(text_lst, nottingham_keyword = 'nottingham'):
    for line in text_lst:
        if nottingham_keyword in line:
            notingham_grade = re.split(',', line)
            notingham_grade = notingham_grade[0]
            notingham_grade = re.sub('\D', '', str(notingham_grade))
            return notingham_grade

def get_notthingham_score(text_lst, nottingham_score_keyword = 'nottingham'):
    try:
        for line in text_lst:
            if nottingham_score_keyword in line:
                notingham_score = re.split(',', line)
                notingham_score = notingham_score[1]
                notingham_score = re.sub('score', '', notingham_score)
                notingham_score = re.sub(':', '', notingham_score)
                return notingham_score
    except IndexError:
        return None

score = get_notthingham_score(unique_text_lst, 'nottingham')

def get_er_status(text_lst, er_keyword = ['positive/negative', 'positive/negatve', 'aled', 'allred']):
    for line in text_lst:
        if any(x in line for x in er_keyword):
            er_txt = re.sub(r'[^a-zA-Z /]', '', str(line))
            cleaned_er_status = re.sub('positive/negative', '', er_txt)
            cleaned_er_status = re.sub('positive/negatve', '', cleaned_er_status)
            cleaned_er_status = re.sub('aled', '', cleaned_er_status)
            cleaned_er_status = re.sub('allred', '', cleaned_er_status)
            cleaned_er_status = re.sub('score', '', cleaned_er_status)
            return cleaned_er_status

status = get_er_status(unique_text_lst, ['positive/negative', 'positive/negatve', 'aled', 'allred'])

def get_keyword_info(file_text_lst, keyword = ['positive/negative', 'positive/negatve', 'intensity']):
    keyword_info = []
    for line in file_text_lst:
        if any(x in line for x in keyword):
            keyword_info.append(line)
    return keyword_info


def get_pr_status(text_lst, pr_keyword = ['positive/negative', 'positive/negatve', 'intensity'], er_status = 'pose'):
    keyword_info = get_keyword_info(text_lst, pr_keyword)
    pr_txt = re.sub(r'[^a-zA-Z /]', '', str(keyword_info))
    cleaned_pr_status = re.sub('positive/negative', '', pr_txt)
    cleaned_pr_status = re.sub('positive/negatve', '', cleaned_pr_status)
    cleaned_pr_status = re.sub('aled', '', cleaned_pr_status)
    cleaned_pr_status = re.sub('allred', '', cleaned_pr_status)
    cleaned_pr_status = re.sub('score', '', cleaned_pr_status)
    cleaned_pr_status = re.sub('intensity', '', cleaned_pr_status)
    cleaned_pr_status = re.sub(er_status, '', cleaned_pr_status)
    return cleaned_pr_status

pr_status = get_pr_status(text_lst, ['positive/negative', 'positive/negatve', 'intensity'])

def get_her2_status(text_lst, her2_keyword = 'her-2/neu'):
    for line in text_lst:
        if her2_keyword in line:
            her2_index = text_lst.index(line)
            her2_status = text_lst[her2_index + 1]
            return her2_status

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

def get_report_information(txt_folder_path, sid_keyword = 'sid', cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin','calcium', 'phosphorus', 'urea', 'serum'],
                           sample_dt_keyword = 'sample date', age_str = 'years', gender_str = 'sex',
                           specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis',
                           nottingham_grade_keyword = 'nottingham', nottingham_score_keyword = 'nottingham',
                           er_keyword = ['positive/negative', 'positive/negatve', 'aled', 'allred'],
                           pr_keyword = ['positive/negative', 'positive/negatve', 'intensity'], her2_keyword = 'her-2/neu'):
    file_names = os.listdir(txt_folder_path)
    report_names = []
    report_types = []
    sids = []
    patient_names = []
    sample_dates = []
    ages = []
    genders = []
    specimen_info_lst = []
    diagnosis_lst = []
    nottingham_grade = []
    nottingham_score = []
    er_status_lst = []
    pr_status_lst = []
    her2_status_lst = []
    for file_name in file_names:
        if file_name.endswith('.txt'):
            print(file_name)
            report_names.append(file_name)
            file_txt = get_report_text_into_list(os.path.join(txt_folder_path, file_name))
            file_txt_unique = get_unique_value_from_list(file_txt)
            sid = get_sid(file_txt_unique, sid_keyword)
            sids.append(sid)
            patient_name = get_patient_name(file_txt_unique)
            patient_names.append(patient_name)
            report_type = classify_report_by_type(file_txt_unique, cytology_keyword, histology_keyword, ihc_keyword,
                                                 blood_count_keyword,
                                                  ki_keyword, glucose_keyword, liver_keyword,
                                                  nutrient_keyword
                                                  )
            report_types.append('; '.join([str(info) for info in report_type]))
            sample_date = get_sample_date(file_txt_unique, sample_dt_keyword)
            sample_dates.append(sample_date)
            age = get_age(file_txt_unique, age_str)
            ages.append(age)
            gender = get_gender(file_txt_unique, gender_str)
            genders.append(gender)
            specimen_info = get_specimen(file_txt_unique, specimen_keyword)
            specimen_info_lst.append(specimen_info)
            diagnosis = get_diagnosis(file_txt_unique, diagnosis_keyword)
            diagnosis_lst.append(diagnosis)
            grade = get_notthingham_grade(file_txt_unique, nottingham_grade_keyword)
            nottingham_grade.append(grade)
            score = get_notthingham_score(file_txt_unique, nottingham_score_keyword)
            nottingham_score.append(score)
            er_status = get_er_status(file_txt_unique, er_keyword)
            er_status_lst.append(er_status)
            er_status_str = str(er_status)
            pr_status = get_pr_status(file_txt_unique, pr_keyword, er_status_str)
            pr_status_lst.append(pr_status)
            her2_status = get_her2_status(file_txt_unique, her2_keyword)
            her2_status_lst.append(her2_status)
    output_df = pd.DataFrame(report_names, columns=['report_name'])
    output_df['report_type'] = report_types
    output_df['lab_sid'] = sids
    output_df['patient_name'] = patient_names
    output_df['sample_date'] = sample_dates
    output_df['age'] = ages
    output_df['gender'] = genders
    output_df['specimen'] = specimen_info_lst
    output_df['diagnosis'] = diagnosis_lst
    output_df['nottingham_grade'] = nottingham_grade
    output_df['nottingham_score'] = nottingham_score
    # output_df['er_status'] = er_status_lst
    # output_df['pr_status'] = pr_status_lst
    # output_df['her2_status'] = her2_status_lst
    return output_df

output_df = get_report_information(txt_files_folder_path, sid_keyword = 'sid', cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin','calcium', 'phosphorus', 'urea', 'serum'],
                            sample_dt_keyword = 'sample date', age_str = 'years', gender_str = 'sex',
                            specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis',
                            nottingham_grade_keyword = 'nottingham', nottingham_score_keyword = 'nottingham',
                            er_keyword=['positive/negative', 'positive/negatve', 'aled', 'allred'],
                            pr_keyword=['positive/negative', 'positive/negatve', 'intensity'],
                            her2_keyword='her-2/neu')

output_df.to_excel('D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_img_txt_files/output_df/2021_08_20_bx_path_date_sk_1.xlsx',
                   index=False)
