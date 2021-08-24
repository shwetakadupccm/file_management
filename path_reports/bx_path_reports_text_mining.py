import os
import re
import pandas as pd
import datetime
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

# def convert_pdf_to_txt(path):
#     rsrcmgr = PDFResourceManager()
#     retstr = StringIO()
#     # codec = 'utf-8' codec=codec
#     laparams = LAParams(char_margin = 20)
#     device = TextConverter(rsrcmgr, retstr, laparams=laparams)
#     file = open(path, 'rb')
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     password = ""
#     maxpages = 0
#     caching = True
#     pagenos=set()
#
#     for page in PDFPage.get_pages(file, pagenos, maxpages = maxpages, password = password, caching = caching,
#                                   check_extractable = True):
#         print(page)
#         interpreter.process_page(page)
#
#     text = retstr.getvalue()
#     print(text)
#
#     file.close()
#     device.close()
#     retstr.close()
#     return text

def split_text_page_wise(path):
    text = convert_pdf_to_txt(path)
    cleaned_text = text.lower()
    no_of_pages = len(re.findall('page', cleaned_text))
    cleaned_text = cleaned_text.replace('page', '//')
    cleaned_text = re.split('//', cleaned_text)
    return no_of_pages, cleaned_text

no_of_pages, splitted_text = split_text_page_wise(os.path.join(folder_path, file_name))

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

page_wies_text = clean_text_page_wise(splitted_text)

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

    page_no_lst = []
    page_text = []
    page_no = 0
    for page_number, page in enumerate(PDFPage.get_pages(file, pagenos, maxpages = maxpages, password = password, caching = caching,
                                  check_extractable = True)):
        if page_no == page_number:
            print(page_no)
            page_no_lst.append(page_no)
            data = interpreter.process_page(page)
            text = retstr.getvalue()
        # print(text)
            page_text.append(data)

    page_no += 1

    text_df = pd.DataFrame(page_no_lst, columns=['page_number'])
    text_df['page_text'] = page_text
    file.close()
    device.close()
    retstr.close()
    return text_df, text

folder_path = 'D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy'
file_name = '110_18_FNAC_Bx_IHC.pdf'
# file_name = '06_20_Bx.pdf'

text = convert_pdf_to_txt(os.path.join(folder_path, file_name))
text1 = text.replace('\n', '//')
text1 = text1.replace(':', '//')
text1 = text1.replace('.', '//')
text1 = text1.lower()
text1 = re.split('//', text1)
text_df = pd.DataFrame(text1, columns=['text'])

def get_patient_name(file_text_lst):
    patient_name = file_text_lst[0]
    cleaned_patient_name = patient_name.replace('reference', '')
    cleaned_patient_name = re.sub(r'[^a-zA-Z ]', '_', cleaned_patient_name)
    cleaned_patient_name = cleaned_patient_name.replace('_', '')
    return cleaned_patient_name

patient_name = get_patient_name(text1)

def get_sid(file_text_lst, sid_keyword = 'sid'):
    try:
        sid_index = file_text_lst.index(sid_keyword)
        sid = file_text_lst[sid_index + 1]
        return sid
    except ValueError:
        return None

sid = get_sid(text1, 'sid')

def get_bx_date(file_text_lst):
    for line in file_text_lst:
        match = re.search('\d{2}-\d{2}-\d{4}', line)
        if match is not None:
            date = datetime.datetime.strptime(match.group(), '%d-%m-%Y').date()
            print(date)
            return date

get_bx_date(text1)

text1 = get_file_text_into_lst(os.path.join(folder_path, file_name))

def get_keyword_info(file_text_lst, keyword = ['her-2']):
    keyword_info = []
    for line in file_text_lst:
        if any(x in line for x in keyword):
            keyword_info.append(line)
    return keyword_info

keyword_info = get_keyword_info(text1, keyword=['positive/negative'])

def get_her2_status_grade(text_lst, her2_keyword = 'c-erbb-2 (her-2/neu) assay'):
      if her2_keyword in text_lst:
          her2_keyword_index = text_lst.index(her2_keyword)
          her2_status_stats = text_lst[her2_keyword_index:her2_keyword_index+10]
          for her2_status_stat in her2_status_stats:
              print(her2_status_stat)
              if her2_status_stat.endswith('ve'):
                  return her2_status_stat
              elif her2_status_stat.endswith('al'):
                  return her2_status_stat

her2_status = get_her2_status_grade(text1, her2_keyword = 'c-erbb-2 (her-2/neu) assay')

def get_unique_value_from_list(list_with_duplicate_values):
    unique_list = []
    for value in list_with_duplicate_values:
        if value not in unique_list:
            unique_list.append(value)
    return unique_list

def get_specimen_type(text_lst, specimen_keyword = ['specimen']):
    cytology = []
    histology = []
    immunohistochemistry = []
    specimen_info = get_keyword_info(text_lst, specimen_keyword)
    specimen_info_unique = get_unique_value_from_list(specimen_info)
    specimen_info_unique_str = str(specimen_info_unique)
    if 'fnac' in specimen_info_unique_str:
        cytology.append('Yes')
    if 'biopsy' in specimen_info_unique_str:
        histology.append('Yes')
    if 'paraffin block' in specimen_info_unique_str:
        immunohistochemistry.append('Yes')
    return specimen_info_unique, cytology, histology, immunohistochemistry

specimen_info, cytology, histology, immunohistochemistry = get_specimen_type(text1, specimen_keyword = ['specimen', 'fnac', 'biopsy', 'block'])

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

er_status = get_er_status(keyword_info)

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


tils_str = ['infiltration', 'stroma']
keyword_info = get_keyword_info(text1, keyword = tils_str)

def get_tils_status(keyword_info, tils_status_types = ['moderate', 'mild', 'marked']):
    for line in keyword_info:
        if any(x in line for x in tils_status_types):
            split_line = line.split(' ')
            print(split_line)
            for word in split_line:
                if any(x in word for x in tils_status_types):
                    return word

tils_status = get_tils_status(keyword_info, ['moderate', 'mild'])

def get_keyword_information_from_report(folder_path, er_pr_keyword = ['positive/negative'], sid_keyword = 'sid',
                                        her2_keyword = 'c-erbb-2 (her-2/neu) assay', tils_keyword = ['infiltration', 'stroma'],
                                        tils_status_types = ['moderate', 'mild', 'marked'], specimen_keyword=['specimen', 'block', 'fnac', 'biopsy']):
    file_names = os.listdir(folder_path)
    sids = []
    patient_names = []
    bx_dates = []
    report_names = []
    specimen_info_lst = []
    cytology_lst = []
    histology_lst = []
    immunohistochemistry_lst = []
    er_keyword_info = []
    er_status_lst = []
    pr_keyword_info = []
    pr_status_lst = []
    her2_status_lst = []
    tils_info_lst = []
    tils_status_lst = []
    for file_name in file_names:
        print(file_name)
        if file_name.endswith('.pdf'):
            report_names.append(file_name)
            file_path = os.path.join(folder_path, file_name)
            file_text = get_file_text_into_lst(file_path)
            sid = get_sid(file_text, sid_keyword)
            sids.append(sid)
            patient_name = get_patient_name(file_text)
            patient_names.append(patient_name)
            bx_date = get_bx_date(file_text)
            bx_dates.append(bx_date)
            specimen_type_info, cytology, histology, immunohistochemistry = get_specimen_type(file_text, specimen_keyword)
            specimen_info_lst.append('; '.join([str(info) for info in specimen_type_info]))
            cytology_lst.append('; '.join([str(info) for info in cytology]))
            histology_lst.append('; '.join([str(info) for info in histology]))
            immunohistochemistry_lst.append('; '.join([str(info) for info in immunohistochemistry]))
            er_info = get_keyword_info(file_text, er_pr_keyword)
            er_info_unique = get_unique_value_from_list(er_info)
            er_keyword_info.append('; '.join([str(info) for info in er_info_unique]))
            er_status = get_er_status(er_info_unique)
            er_status_lst.append(er_status)
            pr_info = get_keyword_info(file_text, er_pr_keyword)
            pr_info_unique = get_unique_value_from_list(pr_info)
            pr_keyword_info.append('; '.join([str(info) for info in pr_info_unique]))
            pr_status = get_pr_status(pr_info_unique)
            pr_status_lst.append(pr_status)
            her2_status = get_her2_status_grade(file_text, her2_keyword)
            her2_status_lst.append(her2_status)
            tils_info = get_keyword_info(file_text, tils_keyword)
            tils_info_unique = get_unique_value_from_list(tils_info)
            tils_info_lst.append('; '.join([str(info) for info in tils_info_unique]))
            tils_status = get_tils_status(tils_info_unique, tils_status_types)
            tils_status_lst.append(tils_status)
    output_df = pd.DataFrame(report_names, columns=['report_name'])
    output_df['patient_name'] = patient_names
    output_df['bx_date'] = bx_dates
    output_df['lab_sid'] = sids
    output_df['specimen_info'] = specimen_info_lst
    output_df['cytology'] = cytology_lst
    output_df['histology'] = histology_lst
    output_df['immunohistochemistry'] = immunohistochemistry_lst
    output_df['er_info'] = er_keyword_info
    output_df['er_status'] = er_status_lst
    output_df['pr_info'] = pr_keyword_info
    output_df['pr_status'] = pr_status_lst
    output_df['her2_status'] = her2_status_lst
    output_df['tils_info'] = tils_info_lst
    output_df['tils_status'] = tils_status_lst
    return output_df

df = get_keyword_information_from_report(folder_path, er_pr_keyword = ['positive/negative'],
                                         her2_keyword = 'c-erbb-2 (her-2/neu) assay', sid_keyword = 'sid',
                                         tils_keyword=['infiltration', 'stroma'], tils_status_types = ['moderate', 'mild', 'marked', 'moderat e'],
                                         specimen_keyword=['specimen', 'block', 'fnac', 'biopsy'])

df.to_excel('D:\\Shweta\\path_reports\\2021_08_10_bx_path_reports\\2021_08_17_patient_name_specimen_bx_er_pr_her2_tils_status_sk.xlsx', index=False)

