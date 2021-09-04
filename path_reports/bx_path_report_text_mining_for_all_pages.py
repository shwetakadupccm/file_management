import re
import pandas as pd
import os
import datetime

pdf_folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy'
# txt_files_folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_img_txt_files'
txt_folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/txt_files_after_removing_lines'

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
            line_txt_cleaned = re.sub('er/pr negative', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('er/ppr negative', '', line_txt_cleaned)
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

text_lst = get_report_text_into_list(os.path.join(txt_folder_path, '110_18_fnac_bx_ihc_3.txt'))
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
    cleaned_patient_name = re.sub('right side', '', cleaned_patient_name)
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

specimen = get_specimen(unique_text_lst, specimen_keyword = 'specimen')

def get_block_id(specimen):
    block_id = re.sub('specimen', '', specimen)
    block_id = re.sub('paraffin', '', block_id)
    block_id = re.sub('block', '', block_id)
    block_id = re.sub('labelled', '', block_id)
    block_id = re.sub('as', '', block_id)
    block_id = re.sub(':', '', block_id)
    block_id = re.sub('_', '', block_id)
    block_id = re.sub('=', '', block_id)
    block_id = re.sub('|', '', block_id)
    block_id = re.sub('left', '', block_id)
    block_id = re.sub('of', '', block_id)
    block_id = re.sub('bret', '', block_id)
    block_id = re.sub('lump.', '', block_id)
    block_id = re.sub('right', '', block_id)
    block_id = re.sub('axillary', '', block_id)
    block_id = re.sub('lymph', '', block_id)
    block_id = re.sub('node', '', block_id)
    block_id = re.sub('biopsy', '', block_id)
    block_id = re.sub('axill', '', block_id)
    return block_id

block_id = get_block_id(specimen)

def get_ihc_no(text_lst, ihc_keywprd = 'ihc'):
    for line in text_lst:
        if ihc_keywprd in line:
            line_idx = text_lst.index(line)
            ihc_id_txt = text_lst[line_idx]
            ihc_id = re.sub('hp', '', str(ihc_id_txt))
            ihc_id = re.sub('no', '', ihc_id)
            ihc_id = re.sub('ihc', '', ihc_id)
            ihc_id = re.sub(':', '', ihc_id)
            return ihc_id

ihc_no = get_ihc_no(unique_text_lst, 'ihc')

def get_cyto_no(text_lst, cyto_keyword = 'cyto no'):
    for line in text_lst:
        if cyto_keyword in line:
            cyto_no = re.sub('cyto', '', str(line))
            cyto_no = re.sub('no.', '', cyto_no)
            cyto_no = re.sub('no', '', cyto_no)
            return cyto_no

cyto_no = get_cyto_no(unique_text_lst, 'cyto no')

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

def get_er_status(text_lst, er_keyword = 'estrogen'):
    for line in text_lst:
        if er_keyword in line:
            er_line_idx = text_lst.index(line)
            pr_line_idx = er_line_idx + 13
            er_txt = text_lst[er_line_idx:pr_line_idx]
            cleaned_er_status = re.sub(r'[^a-zA-Z /]', '', str(er_txt))
            cleaned_er_status = re.sub('positive/negative', '', cleaned_er_status)
            cleaned_er_status = re.sub('positive/negatve', '', cleaned_er_status)
            cleaned_er_status = re.sub('posilive/negalive', '', cleaned_er_status)
            cleaned_er_status = re.sub('positive/n egative', '', cleaned_er_status)
            cleaned_er_status = re.sub('aled', '', cleaned_er_status)
            cleaned_er_status = re.sub('allred', '', cleaned_er_status)
            cleaned_er_status = re.sub('allired', '', cleaned_er_status)
            cleaned_er_status = re.sub('score', '', cleaned_er_status)
            cleaned_er_status_splitted = cleaned_er_status.split(' ')
            for er_status in cleaned_er_status_splitted:
                if er_status.endswith('ive'):
                    return er_status
                elif er_status.startswith('posi'):
                    return er_status
                elif er_status.startswith('nega'):
                    return er_status

er_status = get_er_status(unique_text_lst, 'estrogen')

def get_er_percent(text_lst, er_keyword = 'estrogen'):
    for line in text_lst:
        if er_keyword in line:
            er_line_idx = text_lst.index(line)
            pr_line_idx = er_line_idx + 13
            er_txt = text_lst[er_line_idx:pr_line_idx]
            proportion = re.search(r"\(([0-9%]+)\)", str(er_txt))
            if proportion is not None:
                return proportion.group(1)

proportion = get_er_percent(unique_text_lst, 'estrogen')

def get_keyword_info(file_text_lst, keyword = ['positive/negative', 'positive/negatve', 'intensity']):
    keyword_info = []
    for line in file_text_lst:
        if any(x in line for x in keyword):
            keyword_info.append(line)
    return keyword_info

def get_pr_status(text_lst, pr_keyword = 'progesterone'):
    for line in text_lst:
        if pr_keyword in line:
            line_idx = text_lst.index(line)
            pr_txt1 = text_lst[line_idx + 1]
            pr_txt2 = text_lst[line_idx + 2]
            pr_txt3 = text_lst[line_idx + 3]
            pr_txt = pr_txt1 + ' ' + pr_txt2 + ' ' + pr_txt3
            cleaned_pr_status = re.sub(r'[^a-zA-Z /]', '', str(pr_txt))
            cleaned_pr_status = re.sub('positive/negative', '', cleaned_pr_status)
            cleaned_pr_status = re.sub('positive/negatve', '', cleaned_pr_status)
            cleaned_pr_status = re.sub('posilive/negalive', '', cleaned_pr_status)
            cleaned_pr_status = re.sub('positive/n egative', '', cleaned_pr_status)
            cleaned_pr_status = re.sub('intensity', '', cleaned_pr_status)
            cleaned_pr_status_splitted = cleaned_pr_status.split(' ')
            for pr_status in cleaned_pr_status_splitted:
                if pr_status.endswith('ive'):
                    return pr_status
                elif pr_status.startswith('posi'):
                    return pr_status
                elif pr_status.startswith('nega'):
                    return pr_status

# proportion = re.search(r"([0-9%]+)\(([0-9%]+)\)", str(pr_txt))

def get_pr_percent(text_lst, pr_keyword = 'progesterone'):
    for line in text_lst:
        if pr_keyword in line:
            pr_line_idx = text_lst.index(line)
            final_line_idx = pr_line_idx + 13
            pr_txt = text_lst[pr_line_idx:final_line_idx]
            proportion = re.search(r"\(([0-9%]+)\)", str(pr_txt))
            if proportion is not None:
                pr_percent = proportion.group(1)
                return pr_percent

pr_proportion = get_pr_percent(unique_text_lst, 'progesterone')

def get_tils_status(text_lst, tils_status_types = ['moderate', 'mild', 'marked']):
    for line in text_lst:
        if any(x in line for x in tils_status_types):
            split_line = line.split(' ')
            for word in split_line:
                if any(x in word for x in tils_status_types):
                    return word

def get_her2_status(text_lst, her2_keyword = 'her-2/neu'):
    for line in text_lst:
        if her2_keyword in line:
            her2_index = text_lst.index(line)
            range_index = her2_index + 14
            her2_txt = text_lst[her2_index:range_index]
            cleaned_pr_status = re.sub(r'[^a-zA-Z]', ' ', str(her2_txt))
            cleaned_pr_status = re.sub('negative no staining or membrane staining', '', cleaned_pr_status)
            cleaned_pr_status = re.sub('negative a weak incomplete membrane staining', '', cleaned_pr_status)
            cleaned_pr_status = re.sub('borderline a weak to moderate complete staining', '', cleaned_pr_status)
            cleaned_pr_status = re.sub('positive a strong complete membrane staining', '', cleaned_pr_status)
            her2_status_spllited = cleaned_pr_status.split(' ')
            for status in her2_status_spllited:
                if status.endswith('ive'):
                    return status
                elif status.startswith('posi'):
                    return status
                elif status.endswith('nega'):
                    return status
                elif status.startswith('equ'):
                    return status
                elif status.endswith('cal'):
                    return status

her2_status = get_her2_status(unique_text_lst, 'her-2/neu')

# def get_her2_grade(text_lst, her2_keyword = 'her-2/neu'):
#     for line in text_lst:
#         if her2_keyword in line:
#             her2_index = text_lst.index(line)
#             range_index = her2_index + 14
#             her2_txt = text_lst[her2_index:range_index]
#             for line in her2_txt:
#                 print(line)
#                 if 'score' in line:
#                     line_index = her2_txt.index(line)
#                     her2_grade = re.sub('[^0-9+]', '', str(line))
#                     if her2_grade is not None:
#                         return her2_grade
#                     else:
#                         second_line_txt = her2_txt[line_index + 1]
#                         her2_grade = re.sub('[^0-9+]', '', str(second_line_txt))
#                         return her2_grade

def get_her2_grade(text_lst, her2_keyword = 'her-2/neu'):
    unwanted_txt = {'score her-2 protein staining pattern', '1+ negative a weak incomplete membrane staining',
                    '2+ borderline a weak to moderate complete staining', '3+ positive a strong complete membrane staining',
                    'for equivocal cases (2+) fluorescent in-situ hybridization (fish) analysis for her-2 gene amplification',
                    'c-erbb-2 (her-2/neu) assay', 'in > 30% of tumour cells'}
    for line in text_lst:
        if her2_keyword in line:
            her2_index = text_lst.index(line)
            range_index = her2_index + 14
            her2_txt = text_lst[her2_index:range_index]
            # her2_txt = str(her2_txt)
            her2_txt_cleaned = [txt for txt in her2_txt if txt not in unwanted_txt]
            her2_grade = re.search('[+()\d-]+', str(her2_txt_cleaned))
            return her2_grade.group(0)

her2_grade = get_her2_grade(unique_text_lst, 'her-2/neu')

# def get_her2_grade(text_lst, her2_keyword = 'her-2/neu'):
#     for line in text_lst:
#         if her2_keyword in line:
#             her2_index = text_lst.index(line)
#             range_index = her2_index + 14
#             her2_txt = text_lst[her2_index:range_index]
#             # her2_txt = str(her2_txt)
#             if 'score her-2 protein staining pattern' in her2_txt:
#                 her2_txt.remove('score her-2 protein staining pattern')
#             elif '1+ negative a weak incomplete membrane staining' in her2_txt:
#                 her2_txt.remove('1+ negative a weak incomplete membrane staining')
#             elif '2+ borderline a weak to moderate complete staining' in her2_txt:
#                 her2_txt.remove('2+ borderline a weak to moderate complete staining')
#             elif '3+ positive a strong complete membrane staining' in her2_txt:
#                 her2_txt.remove('3+ positive a strong complete membrane staining')
#             elif 'for equivocal cases (2+) fluorescent in-situ hybridization (fish) analysis for her-2 gene amplification' in text_lst:
#                 her2_txt.remove('for equivocal cases (2+) fluorescent in-situ hybridization (fish) analysis for her-2 gene amplification')
#             elif 'c-erbb-2 (her-2/neu) assay' in her2_txt:
#                 her2_txt.remove('c-erbb-2 (her-2/neu) assay')
#             elif 'in > 30% of tumour cells' in her2_txt:
#                 her2_txt.remove('in > 30% of tumour cells')
#             her2_grade = re.search('[+()\d-]+', str(her2_txt))
#             print(her2_grade)
#             return her2_grade.group(0)
#


def classify_report_by_type(text_lst, cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum']):
    text_lst_str = str(text_lst)
    if cytology_keyword in text_lst_str:
        return 'cytology'
    elif histology_keyword in text_lst_str:
        return 'histology'
    elif ihc_keyword in text_lst_str:
        return 'immunohistochemistry'
    elif blood_count_keyword in text_lst_str:
        return 'complete_blood_count'
    elif ki_keyword in text_lst_str:
        return 'ki67'
    elif glucose_keyword in text_lst_str:
        return 'plasma_glucose'
    elif any(x in text_lst_str for x in nutrient_keyword):
        return 'nutrient_report'
    elif liver_keyword in text_lst_str:
        return 'liver_function_test'
    else:
        return 'type_not_found'

def get_identification_data(file_txt_unique, sid_keyword = 'sid', sample_dt_keyword = 'sample date',
                            age_str = 'years', gender_str = 'sex'):
    sid = get_sid(file_txt_unique, sid_keyword)
    patient_name = get_patient_name(file_txt_unique)
    sample_date = get_sample_date(file_txt_unique, sample_dt_keyword)
    age = get_age(file_txt_unique, age_str)
    gender = get_gender(file_txt_unique, gender_str)
    identification_data = [sid, patient_name, sample_date, age, gender]
    return identification_data

id_data = get_identification_data(unique_text_lst, sid_keyword = 'sid', sample_dt_keyword = 'sample date',
                            age_str = 'years', gender_str = 'sex')

def get_histology_data(file_txt_unique, diagnosis_keyword = 'diagnosis', specimen_keyword = 'specimen',
                       nottingham_grade_keyword = 'nottingham', nottingham_score_keyword = 'nottingham',
                       tils_status_types = ['moderate', 'mild', 'marked']):
    specimen = get_specimen(file_txt_unique, specimen_keyword)
    diagnosis = get_diagnosis(file_txt_unique, diagnosis_keyword)
    tils_status = get_tils_status(file_txt_unique, tils_status_types)
    grade = get_notthingham_grade(file_txt_unique, nottingham_grade_keyword)
    score = get_notthingham_score(file_txt_unique, nottingham_score_keyword)
    histo_data = [specimen, diagnosis, grade, score, tils_status]
    return histo_data

def get_cytology_data(file_txt_unique, diagnosis_keyword = 'diagnosis', specimen_keyword = 'specimen',
                      cyto_keyword = 'cyto no'):
    specimen = get_specimen(file_txt_unique, specimen_keyword)
    diagnosis = get_diagnosis(file_txt_unique, diagnosis_keyword)
    cyto_no = get_cyto_no(file_txt_unique, cyto_keyword)
    cyto_data = [specimen, diagnosis, cyto_no]
    return cyto_data

def get_ihc_data(file_txt_unique, specimen_keyword = 'specimen', er_keyword = 'estrogen', pr_keyword = 'progesterone',
                 her2_keyword = 'her-2/neu', ihc_no_keyword = 'ihc'):
    specimen_info = get_specimen(file_txt_unique, specimen_keyword)
    block_id = get_block_id(specimen_info)
    ihc_no = get_ihc_no(file_txt_unique, ihc_no_keyword)
    er_status = get_er_status(file_txt_unique, er_keyword)
    er_percent = get_er_percent(file_txt_unique, er_keyword)
    pr_status = get_pr_status(file_txt_unique, pr_keyword)
    pr_percent = get_pr_percent(file_txt_unique, pr_keyword)
    if pr_status is None and er_status is not None:
        pr_status = er_status
    her2_status = get_her2_status(file_txt_unique, her2_keyword)
    her2_grade = get_her2_grade(file_txt_unique, her2_keyword)
    ihc_data_list = [specimen_info, block_id, ihc_no, er_status, er_percent, pr_status, pr_percent, her2_status, her2_grade]
    return ihc_data_list

def get_report_data_of_all_pages(txt_folder_path, sid_keyword = 'sid', cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', ihc_no_keyword = 'ihc', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum'],
                           sample_dt_keyword = 'sample date', age_str = 'years', gender_str = 'sex',
                           cyto_keyword = 'cyto no', specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis',
                           tils_status_types = ['moderate', 'mild', 'marked'], nottingham_grade_keyword = 'nottingham',
                           nottingham_score_keyword = 'nottingham', er_keyword = 'estrogen', pr_keyword = 'progesterone',
                           her2_keyword = 'her-2/neu'):
    file_names = os.listdir(txt_folder_path)
    extracted_histo_data = []
    extracted_cyto_data = []
    extracted_ihc_data = []
    for file_name in file_names:
        if file_name.endswith('.txt'):
            print(file_name)
            file_txt = get_report_text_into_list(os.path.join(txt_folder_path, file_name))
            file_txt_unique = get_unique_value_from_list(file_txt)
            identification_data = get_identification_data(file_txt_unique, sid_keyword, sample_dt_keyword,
                            age_str, gender_str)
            identification_data.insert(0, file_name)
            print(identification_data)
            report_type = classify_report_by_type(file_txt_unique, cytology_keyword, histology_keyword, ihc_keyword,
                                blood_count_keyword, ki_keyword, glucose_keyword, liver_keyword, nutrient_keyword)
            if report_type == 'cytology':
                cyto_data_lst = get_cytology_data(file_txt_unique, diagnosis_keyword, specimen_keyword, cyto_keyword)
                cytology_data = identification_data + cyto_data_lst
                extracted_cyto_data.append(cytology_data)
            elif report_type == 'histology':
                histo_lst = get_histology_data(file_txt_unique, diagnosis_keyword, specimen_keyword,
                       nottingham_grade_keyword, nottingham_score_keyword, tils_status_types)
                histology_data = identification_data + histo_lst
                extracted_histo_data.append(histology_data)
            elif report_type == 'immunohistochemistry':
                ihc_lst = get_ihc_data(file_txt_unique, specimen_keyword, er_keyword, pr_keyword,
                            her2_keyword, ihc_no_keyword)
                ihc_data = identification_data + ihc_lst
                extracted_ihc_data.append(ihc_data)
    cyto_df = pd.DataFrame(extracted_cyto_data, columns=['report_name', 'lab_sid', 'patient_name', 'sample_date',
                                                         'age', 'gender', 'specimen', 'diagnosis', 'cyto_no'])
    histo_df = pd.DataFrame(extracted_histo_data, columns=['report_name', 'lab_sid', 'patient_name', 'sample_date',
                                                         'age', 'gender', 'specimen', 'diagnosis', 'nottingham_grade',
                                                           'nottingham_score', 'tils_status'])
    ihc_df = pd.DataFrame(extracted_ihc_data, columns=['report_name', 'lab_sid', 'patient_name', 'sample_date',
                                                         'age', 'gender', 'specimen', 'block_id', 'ihc_no', 'er_status',
                                                       'er_percent', 'pr_status', 'pr_percent', 'her2_status', 'her2_grade'])
    return cyto_df, histo_df, ihc_df

cyto_df, histo_df, ihc_df = get_report_data_of_all_pages(txt_folder_path, sid_keyword = 'sid', cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', ihc_no_keyword = 'ihc', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum'],
                           sample_dt_keyword = 'sample date', age_str = 'years', gender_str = 'sex',
                           cyto_keyword = 'cyto no', specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis',
                           tils_status_types = ['moderate', 'mild', 'marked'], nottingham_grade_keyword = 'nottingham',
                           nottingham_score_keyword = 'nottingham', er_keyword = 'estrogen', pr_keyword = 'progesterone',
                           her2_keyword = 'her-2/neu')

writer = pd.ExcelWriter('D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy\\txt_files_after_removing_lines\\output_df\\2021_09_04_all_bx_path_data_sk.xlsx',
                        engine='xlsxwriter')

cyto_df.to_excel(writer, sheet_name='cytology', index=False)
histo_df.to_excel(writer, sheet_name='histology', index=False)
ihc_df.to_excel(writer, sheet_name='immunohistochemistry', index=False)
writer.save()

def get_report_information(txt_folder_path, sid_keyword = 'sid', cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', ihc_no_keyword = 'ihc', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum'],
                           sample_dt_keyword = 'sample date', age_str = 'years', gender_str = 'sex',
                           cyto_keyword = 'cyto no', specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis',
                           tils_status_types = ['moderate', 'mild', 'marked'], nottingham_grade_keyword = 'nottingham',
                           nottingham_score_keyword = 'nottingham', er_keyword = 'estrogen', pr_keyword = 'progesterone',
                           her2_keyword = 'her-2/neu'):
    file_names = os.listdir(txt_folder_path)
    extracted_txt_lst = []
    for file_name in file_names:
        if file_name.endswith('.txt'):
            print(file_name)
            file_txt = get_report_text_into_list(os.path.join(txt_folder_path, file_name))
            file_txt_unique = get_unique_value_from_list(file_txt)
            sid = get_sid(file_txt_unique, sid_keyword)
            patient_name = get_patient_name(file_txt_unique)
            report_type = classify_report_by_type(file_txt_unique, cytology_keyword, histology_keyword, ihc_keyword,
                                                 blood_count_keyword,
                                                  ki_keyword, glucose_keyword, liver_keyword,
                                                  nutrient_keyword
                                                  )
            sample_date = get_sample_date(file_txt_unique, sample_dt_keyword)
            age = get_age(file_txt_unique, age_str)
            gender = get_gender(file_txt_unique, gender_str)
            specimen_info = get_specimen(file_txt_unique, specimen_keyword)
            tils_status = get_tils_status(file_txt_unique, tils_status_types)
            block_id = get_block_id(specimen_info)
            ihc_no = get_ihc_no(unique_text_lst, ihc_no_keyword)
            cyto_no = get_cyto_no(unique_text_lst, cyto_keyword)
            diagnosis = get_diagnosis(file_txt_unique, diagnosis_keyword)
            grade = get_notthingham_grade(file_txt_unique, nottingham_grade_keyword)
            score = get_notthingham_score(file_txt_unique, nottingham_score_keyword)
            er_status = get_er_status(file_txt_unique, er_keyword)
            er_percent = get_er_percent(file_txt_unique, er_keyword)
            pr_status = get_pr_status(file_txt_unique, pr_keyword)
            pr_percent = get_pr_percent(file_txt_unique, pr_keyword)
            her2_status = get_her2_status(file_txt_unique, her2_keyword)
            her2_grade = get_her2_grade(file_txt_unique, her2_keyword)
            if pr_status is None and er_status is not None:
                pr_status = er_status
            txt_lst = [file_name, patient_name, sid, report_type, sample_date, age, gender, specimen_info, tils_status,
                       block_id, ihc_no, cyto_no, diagnosis, grade, score, er_status, er_percent, pr_status, pr_percent, her2_status,
                       her2_grade]
            extracted_txt_lst.append(txt_lst)
            colnames = ['report_name', 'patient_name', 'lab_sid', 'report_type', 'sample_date', 'age', 'gender', 'specimen',
                        'tils_status', 'block_id', 'ihc_no', 'cyto_no', 'diagnosis', 'nottingham_grade', 'nottingham_score', 'er_status', 'er_percent', 'pr_status',
                        'pr_percent', 'her2_status', 'her2_grade']
    output_df = pd.DataFrame(extracted_txt_lst, columns=colnames)
    return output_df

output_df = get_report_information(txt_folder_path, sid_keyword = 'sid', cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin','calcium', 'phosphorus', 'urea', 'serum'],
                            sample_dt_keyword = 'sample date', age_str = 'years', gender_str = 'sex', cyto_keyword = 'cyto no',
                            specimen_keyword = 'specimen', diagnosis_keyword = 'diagnosis', tils_status_types = ['moderate', 'mild', 'marked'],
                            nottingham_grade_keyword = 'nottingham', nottingham_score_keyword = 'nottingham',
                            er_keyword='estrogen', pr_keyword='progesterone', her2_keyword='her-2/neu')

output_df.to_excel('D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/txt_files_after_removing_lines/output_df/2021_09_03_bx_path_data_sk.xlsx',
                   index=False)
