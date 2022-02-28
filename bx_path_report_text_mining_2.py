import os
import re
import pandas as pd
import datetime
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

folder_path = 'D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy'
file_name = '110_18_FNAC_Bx_IHC.pdf'

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    # codec = 'utf-8' codec=codec
    laparams = LAParams(char_margin = 20)
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    file = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(file, pagenos, maxpages = maxpages, password = password, caching = caching,
                                  check_extractable = True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    file.close()
    device.close()
    retstr.close()
    return text

text = convert_pdf_to_txt(os.path.join(folder_path, file_name))

def split_text_page_wise(path):
    text = convert_pdf_to_txt(path)
    cleaned_text = text.lower()
    no_of_pages = len(re.findall('page', cleaned_text))
    cleaned_text = cleaned_text.replace('page', '//')
    cleaned_text = re.split('//', cleaned_text)
    return cleaned_text

spllited_text = split_text_page_wise(os.path.join(folder_path, file_name))

def get_file_text_into_lst(path):
    text = convert_pdf_to_txt(path)
    text1 = text.replace('\n', '//')
    text1 = text1.replace(':', '//')
    text1 = text1.replace('.', '//')
    text1 = text1.lower()
    text1 = re.split('//', text1)
    return text1

def clean_text_page_wise(splitted_text_page_wise):
    page_wise_text = []
    for page_text in splitted_text_page_wise:
        text = page_text.replace('\n', '//')
        text = text.replace(':', '//')
        text = text.replace('.', '//')
        text = text.lower()
        text = re.split('//', text)
        page_wise_text.append(', '.join([str(info) for info in text]))
    return page_wise_text

def clean_text_page_wise(splitted_text_page_wise):
    page_wise_text = []
    for page_text in splitted_text_page_wise:
        text = page_text.replace('\n', '//')
        text = text.replace(':', '//')
        text = text.replace('.', '//')
        text = text.lower()
        text = re.split('//', text)
        page_wise_text.append(', '.join([str(info) for info in text]))
    return page_wise_text

page_wise_text = clean_text_page_wise(spllited_text)

def get_patient_name(file_text_lst):
    patient_name = file_text_lst[0]
    cleaned_patient_name = patient_name.replace('reference', '')
    cleaned_patient_name = re.sub(r'[^a-zA-Z ]', '_', cleaned_patient_name)
    cleaned_patient_name = cleaned_patient_name.replace('_', '')
    return cleaned_patient_name

def get_sid(file_text_lst, sid_keyword = 'sid'):
    try:
        sid_index = file_text_lst.index(sid_keyword)
        sid = file_text_lst[sid_index + 1]
        return sid
    except ValueError:
        return None

def get_bx_date(file_text_lst):
    for line in file_text_lst:
        match = re.search('\d{2}-\d{2}-\d{4}', line)
        if match is not None:
            date = datetime.datetime.strptime(match.group(), '%d-%m-%Y').date()
            return date

def get_keyword_info(file_text_lst, keyword = ['her-2']):
    keyword_info = []
    for line in file_text_lst:
        if any(x in line for x in keyword):
            keyword_info.append(line)
    return keyword_info

def get_her2_status_grade(text_lst, her2_keyword='c-erbb-2 (her-2/neu) assay'):
    if her2_keyword in text_lst:
        her2_keyword_index = text_lst.index(her2_keyword)
        her2_status_stats = text_lst[her2_keyword_index:her2_keyword_index + 10]
        for her2_status_stat in her2_status_stats:
            if her2_status_stat.endswith('ve'):
                return her2_status_stat
            elif her2_status_stat.endswith('al'):
                return her2_status_stat

def get_unique_value_from_list(list_with_duplicate_values):
    unique_list = []
    for value in list_with_duplicate_values:
        if value not in unique_list:
            unique_list.append(value)
    return unique_list

# def get_specimen_type(text_lst, specimen_keyword = ['specimen']):
#     cytology = []
#     histology = []
#     immunohistochemistry = []
#     specimen_info = get_keyword_info(text_lst, specimen_keyword)
#     specimen_info_unique = get_unique_value_from_list(specimen_info)
#     specimen_info_unique_str = str(specimen_info_unique)
#     if 'fnac' in specimen_info_unique_str:
#         cytology.append('Yes')
#     if 'biopsy' in specimen_info_unique_str:
#         histology.append('Yes')
#     if 'paraffin block' in specimen_info_unique_str:
#         immunohistochemistry.append('Yes')
#     return specimen_info_unique, cytology, histology, immunohistochemistry

def get_er_status(keyword_info, keyword_for_er_status = ['allred score', 'quick score']):
    if keyword_info is not None:
        for line in keyword_info:
            if any(x in line for x in keyword_for_er_status):
                try:
                    er_status = re.sub('positive/negative', '', line)
                    er_status = re.sub(r'[^a-zA-Z ]', '', er_status)
                    er_status = re.sub('allred score', '', er_status)
                    er_status = re.sub('quick score', '', er_status)
                    return er_status
                except TypeError:
                    return None

def get_pr_status(keyword_info):
    if keyword_info is not None:
        for line in keyword_info:
            if 'intensity' in line:
                try:
                    pr_status = re.sub('positive/negative', '', line)
                    pr_status = re.sub(r'[^a-zA-Z ]', '', pr_status)
                    pr_status = re.sub('intensity', '', pr_status)
                    return pr_status
                except TypeError:
                    return None

def get_tils_status(keyword_info, tils_status_types = ['moderate', 'mild', 'marked']):
    for line in keyword_info:
        if any(x in line for x in tils_status_types):
            split_line = line.split(' ')
            for word in split_line:
                if any(x in word for x in tils_status_types):
                    return word

def get_identifing_info_from_report(page_text):
    patient_name = get_patient_name(page_text)



def get_keyword_information_from_report(folder_path, er_pr_keyword = ['positive/negative'], sid_keyword = 'sid',
                                        her2_keyword = 'c-erbb-2 (her-2/neu) assay', tils_keyword = ['infiltration', 'stroma'],
                                        tils_status_types = ['moderate', 'mild', 'marked'], specimen_keyword=['specimen', 'block', 'fnac', 'biopsy']):
    file_names = os.listdir(folder_path)
    sids1 = []
    patient_names1 = []
    bx_dates1 = []
    report_names1 = []
    specimen_info_lst1 = []
    er_keyword_info1 = []
    er_status_lst1 = []
    pr_keyword_info1 = []
    pr_status_lst1 = []
    her2_status_lst1 = []
    tils_info_lst1 = []
    tils_status_lst1 = []
    for file_name in file_names:
        print(file_name)
        if file_name.endswith('.pdf'):
            file_path = os.path.join(folder_path, file_name)
            file_text = split_text_page_wise(file_path)
            page_wise_text = clean_text_page_wise(file_text)
            sids = []
            patient_names = []
            bx_dates = []
            specimen_info_lst = []
            report_names = []
            er_keyword_info = []
            er_status_lst = []
            pr_keyword_info = []
            pr_status_lst = []
            her2_status_lst = []
            tils_info_lst = []
            tils_status_lst = []
            for page_text in page_wise_text:
                report_names.append(file_name)
                sid = get_sid(page_text, sid_keyword)
                sids.append(sid)
                patient_name = get_patient_name(page_text)
                patient_names.append(patient_name)
                bx_date = get_bx_date(page_text)
                bx_dates.append(bx_date)
                er_info = get_keyword_info(page_text, er_pr_keyword)
                er_info_unique = get_unique_value_from_list(er_info)
                er_keyword_info.append('; '.join([str(info) for info in er_info_unique]))
                er_status = get_er_status(er_info_unique)
                er_status_lst.append(er_status)
                pr_info = get_keyword_info(page_text, er_pr_keyword)
                pr_info_unique = get_unique_value_from_list(pr_info)
                pr_keyword_info.append('; '.join([str(info) for info in pr_info_unique]))
                pr_status = get_pr_status(pr_info_unique)
                pr_status_lst.append(pr_status)
                her2_status = get_her2_status_grade(page_text, her2_keyword)
                her2_status_lst.append(her2_status)
                tils_info = get_keyword_info(page_text, tils_keyword)
                tils_info_unique = get_unique_value_from_list(tils_info)
                tils_info_lst.append('; '.join([str(info) for info in tils_info_unique]))
                tils_status = get_tils_status(tils_info_unique, tils_status_types)
                tils_status_lst.append(tils_status)
            patient_names1.append(patient_names)
            bx_dates1.append(bx_dates)
            sids1.append(sids)
            specimen_info_lst1.append(specimen_info_lst)
            er_keyword_info1.append(er_keyword_info)
            er_status_lst1.append(er_status_lst)
            pr_keyword_info1.append(pr_keyword_info)
            pr_status_lst1.append(pr_status_lst)
            her2_status_lst1.append(her2_status_lst)
            tils_info_lst1.append(tils_info_lst)
            tils_status_lst1.append(tils_status_lst)
    output_df = pd.DataFrame(report_names1, columns=['report_name'])
    output_df['patient_name'] = patient_names1
    output_df['bx_date'] = bx_dates1
    output_df['lab_sid'] = sids1
    output_df['specimen_info'] = specimen_info_lst1
    output_df['er_info'] = er_keyword_info1
    output_df['er_status'] = er_status_lst1
    output_df['pr_info'] = pr_keyword_info1
    output_df['pr_status'] = pr_status_lst1
    output_df['her2_status'] = her2_status_lst1
    output_df['tils_info'] = tils_info_lst1
    output_df['tils_status'] = tils_status_lst1
    return output_df


df = get_keyword_information_from_report(folder_path, er_pr_keyword = ['positive/negative'],
                                         her2_keyword = 'c-erbb-2 (her-2/neu) assay', sid_keyword = 'sid',
                                         tils_keyword=['infiltration', 'stroma'], tils_status_types = ['moderate', 'mild', 'marked', 'moderat e'],
                                         specimen_keyword=['specimen', 'block', 'fnac', 'biopsy'])
