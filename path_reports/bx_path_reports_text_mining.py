import os
import re
import numpy as np
import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

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

folder_path = 'Z:\\Clinical_Database\\Digitized_Files\\Histopath\\Biopsy'
file_name = '120075656.pdf'

text = convert_pdf_to_txt(os.path.join(folder_path, file_name))
text1 = text.replace('\n', '//')
text1 = text1.replace(':', '//')
text1 = text1.replace('.', '//')
text1 = text1.lower()
text1 = re.split('//', text1)
text_df = pd.DataFrame(text1, columns=['text'])

def get_file_text_into_lst(path):
    text = convert_pdf_to_txt(path)
    text1 = text.replace('\n', '//')
    text1 = text1.replace(':', '//')
    text1 = text1.replace('.', '//')
    text1 = text1.lower()
    text1 = re.split('//', text1)
    return text1

text1 = get_file_text_into_lst(os.path.join(folder_path, file_name))

def get_keyword_info(file_text_lst, keyword = ['her-2']):
    keyword_info = []
    for line in file_text_lst:
        if any(x in line for x in keyword):
            keyword_info.append(line)
    return keyword_info

keyword_info = get_keyword_info(text1, keyword = ['her-2/neu'])
keyword = 'c-erbb-2 (her-2/neu) assay'
text1.index(keyword)

index = keyword_info.index(keyword) + 6
get_her2_line = text1[6]

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

def get_er_pr_status(keyword_info, keyword = 'er/pr'):
    before_keyword, keyword_str, after_keyword = keyword_info.partition(keyword)
    er_pr_status = after_keyword[1:9]
    return er_pr_status

def get_keyword_information_from_report(folder_path, er_pr_keyword = ['her', 'er', 'pr'],
                                        her2_keyword = 'c-erbb-2 (her-2/neu) assay'):
    file_names = os.listdir(folder_path)
    report_names = []
    report_keyword_info = []
    report_keyword_status = []
    her2_status_lst = []
    her2_grade_lst = []
    for file_name in file_names:
        print(file_name)
        if file_name.endswith('.pdf'):
            report_names.append(file_name)
            file_path = os.path.join(folder_path, file_name)
            file_text = get_file_text_into_lst(file_path)
            keyword_info = get_keyword_info(file_text, er_pr_keyword)
            keyword_info_unique = get_unique_value_from_list(keyword_info)
            report_keyword_info.append('; '.join([str(info) for info in keyword_info_unique]))
            keyword_status = get_er_pr_status(str(keyword_info), 'er/pr')
            if keyword_status.endswith('ve'):
                report_keyword_status.append(keyword_status)
            else:
                report_keyword_status.append('not_found')
            her2_status = get_her2_status_grade(file_text, her2_keyword)
            her2_status_lst.append(her2_status)
    output_df = pd.DataFrame(report_names, columns=['report_name'])
    output_df['keyword_info'] = report_keyword_info
    output_df['keyword_status'] = report_keyword_status
    output_df['her2_status'] = her2_status_lst
    return output_df

df = get_keyword_information_from_report(folder_path, er_pr_keyword = ['er/pr'], her2_keyword = 'c-erbb-2 (her-2/neu) assay')

df_her2 = get_keyword_information_from_report(folder_path, er_pr_keyword=['her-2', 'her 2'])

df.to_excel('D:\\Shweta\\path_reports\\2021_08_10_bx_path_reports\\2021_08_12_bx_er_pr_her2_status_sk.xlsx', index=False)

