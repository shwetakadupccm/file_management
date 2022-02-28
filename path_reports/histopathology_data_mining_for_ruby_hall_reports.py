import pandas as pd
import os
import re
import datetime

txt_folder_path = 'D:/Shweta/email/attachments_from_ruby_hall/txt_img'
file_name = 'ob205570_361354_toke rupa satyawan_2.txt'

def get_jpg_file_path(folder_path, file):
    file_name = re.sub('.txt', '.jpg', file)
    file_path = os.path.join(folder_path, file_name)
    return file_name, file_path

# path_df = get_jpg_file_path(txt_folder_path)
#
# path_df.to_excel('D:/Shweta/email/attachments_from_jehangir/jeh_reports_page_img_txt/output_df/2021_09_15_path_sk.xlsx',
#                    index=False)

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

def get_unique_value_from_list(list_with_duplicate_values):
    unique_list = []
    for value in list_with_duplicate_values:
        if value not in unique_list:
            unique_list.append(value)
    output_lst = [line for line in unique_list if line]
    return output_lst

text = get_report_text_into_list(os.path.join(txt_folder_path, file_name))
unique_text = get_unique_value_from_list(text)
text_df = pd.DataFrame(unique_text)

def get_patinet_name(report_text_lst, name_str = 'patient name'):
    for line in report_text_lst:
        if name_str in line:
            patient_name = re.sub('[^A-Za-z ]', '', str(line))
            patient_name = re.sub('patient name', '', patient_name)
            patient_name = re.sub('name', '', patient_name)
            patient_name = re.sub('age', '', patient_name)
            patient_name = re.sub('gender', '', patient_name)
            patient_name = re.sub('yrs', '', patient_name)
            patient_name = re.sub('ys', '', patient_name)
            patient_name = re.sub('female', '', patient_name)
            patient_name = re.sub('male', '', patient_name)
            patient_name = re.sub('mrs', '', patient_name)
            patient_name = re.sub('ms', '', patient_name)
            patient_name = re.sub('mr', '', patient_name)
            patient_name = re.sub('miss', '', patient_name)
            patient_name = patient_name.strip()
            return patient_name

patient_name = get_patinet_name(unique_text, 'name')

def get_uhid_no(report_text_lst, uhid_no_keyword = 'uhid no'):
    for line in report_text_lst:
        if uhid_no_keyword in line:
            uhid_no = re.sub('[^0-9/w]', '', str(line))
            uhid_no = re.sub('admn/', '', uhid_no)
            uhid_no = re.sub('admn /', '', uhid_no)
            return uhid_no

uhid_no = get_uhid_no(unique_text, 'uhid no')

# def get_hpe_no(report_text_lst, hpe_keyword = 'hpe-no'):
#     for line in report_text_lst:
#         if hpe_keyword in line:
#             hpe_line_idx = report_text_lst.index(line)
#             line_idx = hpe_line_idx+2
#             line_txt = report_text_lst[hpe_line_idx:line_idx]
#             hpe_no = re.sub('[^0-9-A-Za-z /-]', '', str(line_txt))
#             hpe_no = re.sub('hpe-', '', hpe_no)
#             hpe_no = re.sub('no', '', hpe_no)
#             hpe_no = hpe_no.strip()
#             return hpe_no

# hpe_no = get_hpe_no(unique_text, 'hpe')

def get_age(text_lst, age_str = 'age'):
    for line in text_lst:
        if age_str in line:
            age = re.sub(r'[^0-9]', '', str(line))
            age = age[0:2]
            return age

age = get_age(unique_text, 'age')

def get_gender(text_lst, gender_str = 'gender'):
    for line in text_lst:
        if gender_str in line:
            gender_txt = re.sub(r'[^a-zA-Z ]', '', str(line))
            spllited_text = gender_txt.split('age')
            cleaned_gender = re.sub('age', '', spllited_text[1])
            cleaned_gender = re.sub('yrs', '', cleaned_gender)
            cleaned_gender = re.sub('ys', '', cleaned_gender)
            cleaned_gender = re.sub('gender', '', cleaned_gender)
            cleaned_gender = re.sub('name', '', cleaned_gender)
            spllited_txt = cleaned_gender.split()
            for value in spllited_txt:
                if value.endswith('ale'):
                    return value

gender = get_gender(unique_text, 'gender')

def get_tagged_date(report_text_lst, tag_str = 'report date'):
    for line in report_text_lst:
        if tag_str in line:
            date_name_index = report_text_lst.index(line)
            date_txt = report_text_lst[date_name_index]
            date_txt_splitted = date_txt.split('report date')
            if date_txt_splitted is not None:
                try:
                    match = re.search(r'\d{2}-([^-\d]+)-\d{4}', date_txt_splitted[1])
                    date = datetime.datetime.strptime(match.group(), '%d-%b-%Y').date()
                    if date is not None:
                        return date
                except AttributeError:
                    return None

string = '07-may-2019 04:36 pm'
match = re.search(r'\d{2}-([^-\d]+)-\d{4}', string)
date = datetime.datetime.strptime(match.group(), '%d-%b-%Y').date()

sc_date = get_tagged_date(unique_text, 'report date')

def get_pt(report_text_lst, pt_keyword = 'primary tumor'):
    for line in report_text_lst:
        if pt_keyword in line:
            pt = re.sub('primary tumor', '', str(line))
            pt = re.sub("[\(\[].*?[\)\]]", '', pt)
            pt = re.sub('-', '', pt)
            pt = pt.upper()
            pt = pt.strip()
            return pt

pt = get_pt(unique_text, '(pt)')

def get_pn(report_text_lst, pn_keyword = 'regional lymph nodes'):
    for line in report_text_lst:
        if pn_keyword in line:
            print(line)
            pn = re.sub('regional', '', str(line))
            pn = re.sub('lymph', '', pn)
            pn = re.sub('nodes', '', pn)
            pn = re.sub('[\(\[].*?[\)\]]', '', pn)
            pn = re.sub('-', '', pn)
            pn = pn.upper()
            pn = pn.strip()
            return pn

pn = get_pn(unique_text, '(pn)')

def get_pathological_stage(report_text_lst,
    pathological_stage_keyword = 'pathologic staging'):
    for line in report_text_lst:
        if pathological_stage_keyword in line:
            pathological_stage = re.sub('pathologic', '', str(line))
            pathological_stage = re.sub('staging', '', pathological_stage)
            pathological_stage = re.sub('-', '', pathological_stage)
            pathological_stage = re.sub('[\(\[].*?[\)\]]', '', pathological_stage)
            pathological_stage = pathological_stage.upper()
            pathological_stage = pathological_stage.strip()
            return pathological_stage


def get_nottingham_score(report_text_lst, nottingham_keyword = ['nottingham', 'modified bloom richardson score']):
    for line in report_text_lst:
        print(line)
        if any(x in line for x in nottingham_keyword):
            nottingham_score = re.sub(r'[^0-9+=/]', '', str(line))
            return nottingham_score

score = get_nottingham_score(unique_text, nottingham_keyword = ['nottingham', 'modified bloom richardson score'])

def get_tumour_size(report_text_lst, tumour_size_keyword = ['tumor size', 'size of invasive carcinoma']):
    for line in report_text_lst:
        if any(x in line for x in tumour_size_keyword):
            tumour_size = re.sub(r'[^0-9x.]', '', str(line))
            return tumour_size

tumour_size = get_tumour_size(unique_text, 'tumor size')

def get_tumour_size_unit(report_text_lst, tumour_size_keyword = ['tumor size', 'size of invasive carcinoma'],
                         units = ['cm', 'mm']):
    for line in report_text_lst:
        if any(x in line for x in tumour_size_keyword):
            tumour_size_unit = re.sub('[^A-Za-z ]', '', str(line))
            tumour_size_unit = re.sub('tumor size', '', tumour_size_unit)
            tumour_size_unit = re.sub('x', '', tumour_size_unit)
            tumour_size_unit = tumour_size_unit.strip()
            tumour_size_unit_splitted = tumour_size_unit.split(' ')
            for splitted_unit in tumour_size_unit_splitted:
                if splitted_unit in units:
                    return splitted_unit

unit = get_tumour_size_unit(unique_text, tumour_size_keyword = ['tumor size', 'size of invasive carcinoma'],
                         units = ['cm', 'mm'])

def get_tils(report_text_lst, tils_keyword = 'tils'):
    for line in report_text_lst:
        if tils_keyword in line:
            tils = re.sub(r'[^0-9%<>]', '', str(line))
            tils = tils.strip()
            return tils

def get_tils_comment(report_text_lst, tils_comment_keyword = 'stroma'):
    for line in report_text_lst:
        if tils_comment_keyword in line:
            comment = re.sub(r'[^a-zA-Z ]', '', str(line))
            comment = comment.strip()
            return comment

comment = get_tils_comment(unique_text, 'stroma')

def get_rcb_index(report_text_lst, rcb_keyword = 'residual cancer burden'):
    for line in report_text_lst:
        if rcb_keyword in line:
            rcb_index = re.sub(rcb_keyword, '', str(line))
            rcb_index = re.sub(r'[^0-9.]', '', rcb_index)
            try:
                if rcb_index[-1] == '.':
                    rcb_index = rcb_index[:-1]
                    rcb_index = float(rcb_index)
                    return rcb_index
                else:
                    rcb_index = float(rcb_index)
                    return rcb_index
            except IndexError:
                return None

rcb = get_rcb_index(text, 'residual cancer burden')

def get_rcb_class(report_text_lst, rcb_keyword = 'residual cancer burden',
                  rcb_classes = ['I','II','III']):
    for line in report_text_lst:
        if rcb_keyword in line:
            rcb_class = re.sub(rcb_keyword, '', str(line))
            rcb_class = re.sub('rcb', '', rcb_class)
            rcb_class = re.sub('index', '', rcb_class)
            rcb_class = re.sub(r'[^a-z]', '', rcb_class)
            rcb_class = re.sub('class', '', rcb_class)
            rcb_class = rcb_class.upper()
            if rcb_class in rcb_classes:
                return rcb_class

rcb_class = get_rcb_class(text, 'residual cancer burden', rcb_classes = ['I','II','III'])

def put_all_report_data_into_one_row(unique_txt_lst):
    list_of_unique_txt = []
    list_of_unique_txt.append(' | '.join([str(x) for x in unique_txt_lst]))
    return list_of_unique_txt

def make_hyperlink(path, file_name):
    url = "{}"
    return '=HYPERLINK("%s", "%s")' % (url.format(path), file_name)

def get_pdf_file_path(pdf_folder_path, file):
    file_name = file[:-6]
    pdf_file_name = file_name + '.pdf'
    file_path = os.path.join(pdf_folder_path, pdf_file_name)
    return pdf_file_name, file_path

# def classify_reports_by_type(unique_txt_lst, histo_keyword = 'histology'):

def get_report_data(txt_folder_path, name_str = 'patient name', age_str = 'age', gender_str = 'gender',
                    tag_str = 'report date', nottingham_keyword = ['nottingham', 'modified bloom richardson score'],
                    uhid_no_keyword = 'reg no', pt_keyword = 'primary tumor',
                    pn_keyword = 'regional lymph nodes', pathological_stage_keyword = 'pathologic staging',
                    tumour_size_keyword = ['tumor size', 'size of invasive carcinoma'],
                    units = ['cm', 'mm'], tils_keyword = 'tils'):
    file_names = os.listdir(txt_folder_path)
    report_data_extracted = []
    for file_name in file_names:
        if file_name.endswith('.txt'):
            print(file_name)
            file_txt = get_report_text_into_list(os.path.join(txt_folder_path, file_name))
            file_txt_unique = get_unique_value_from_list(file_txt)
            jpg_file_name, file_path = get_jpg_file_path(txt_folder_path, file_name)
            hyper_link = make_hyperlink(file_path, jpg_file_name)
            pdf_file_name = file_name[:-6]
            patient_name = get_patinet_name(file_txt_unique, name_str)
            # hpe_no = get_hpe_no(file_txt_unique, hpe_keyword)
            uhid_no = get_uhid_no(file_txt_unique, uhid_no_keyword)
            age = get_age(file_txt_unique, age_str)
            gender = get_gender(file_txt_unique, gender_str)
            report_date = get_tagged_date(file_txt_unique, tag_str)
            tumour_size = get_tumour_size(file_txt_unique, tumour_size_keyword)
            tumour_size_unit = get_tumour_size_unit(file_txt_unique, tumour_size_keyword, units)
            nottingham_score = get_nottingham_score(file_txt_unique, nottingham_keyword)
            tils = get_tils(file_txt_unique, tils_keyword)
            pt = get_pt(file_txt_unique, pt_keyword)
            pn = get_pn(file_txt_unique, pn_keyword)
            pathological_stage = get_pathological_stage(file_txt_unique, pathological_stage_keyword)
            data_extracted = [file_name, pdf_file_name, hyper_link, patient_name, uhid_no, age, gender, report_date,
                              tumour_size, tumour_size_unit, nottingham_score, tils, pt, pn, pathological_stage]
            report_data_extracted.append(data_extracted)
    output_df = pd.DataFrame(report_data_extracted, columns=['report_name', 'pdf_file_name', 'hyperlink_of_jpg_file',
                                                             'patient_name', 'uhid_no', 'age', 'gender',
                                                             'report_date', 'tumour_size', 'tumour_size_unit',
                                                             'nottingham_score', 'tils', 'pT', 'pN',
                                                             'pathological_stage'])
    return output_df

output_df = get_report_data(txt_folder_path, name_str = 'patient name', age_str = 'age', gender_str = 'gender',
                    tag_str = 'report date', nottingham_keyword = ['nottingham', 'modified bloom richardson score'],
                    uhid_no_keyword = 'reg no', pt_keyword = '(pt)',
                    pn_keyword = '(pn)', pathological_stage_keyword = 'pathologic staging',
                    tumour_size_keyword = ['tumor size', 'size of invasive carcinoma'],
                    units = ['cm', 'mm'], tils_keyword = 'tils')

output_df.to_excel('D:/Shweta/email/attachments_from_ruby_hall/txt_img/output_df/2021_09_29_ruby_hall_sx_path_data_with_tils_sk.xlsx',
                         index=False)
