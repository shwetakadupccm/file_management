import os
import re
import pandas as pd
import numpy as np

folder_path = 'D:\\Shweta\\path_reports\\2021_12_07_surgery_path_reports_nact_sk'
file_name = '13_18_Sx_01.pdf'
file_path = os.path.join(folder_path, file_name)
##

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

##

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

    for page in PDFPage.get_pages(file, pagenos, maxpages=maxpages, password=password,caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    file.close()
    device.close()
    retstr.close()
    return text

text = convert_pdf_to_txt(file_path)

text1 = text.replace('\n', '/')
text1 = text1.replace(':', '/')
text1 = text1.lower()
text1 = re.split('/', text1)
# text_df = pd.DataFrame(text1, columns = ['report_text'])
# text_df.to_excel('D:\\Shweta\\path_reports\\output_df_sx_path_reports\\2021_17_07_text_df_sx_path_report.xlsx')

def get_file_text_into_lst(path):
    text = convert_pdf_to_txt(path)
    text1 = text.replace('\n', '/')
    text1 = text1.replace(':', '/')
    text1 = text1.lower()
    text1 = re.split('/', text1)
    return text1

file_text_lst = get_file_text_into_lst(file_path)

def get_keyword_info(file_text_lst, keyword = ['chemo', 'residual', 'nact']):
    keyword_info = []
    for line in file_text_lst:
        if any(x in line for x in keyword):
            keyword_info.append(line)
    return keyword_info

def get_keyword_information_from_report(folder_path, keyword = ['chemo', 'residual', 'nact']):
    file_names = os.listdir(folder_path)
    report_names = []
    report_keyword_info = []
    for file_name in file_names:
        report_names.append(file_name)
        file_path = os.path.join(folder_path, file_name)
        file_text = get_file_text_into_lst(file_path)
        keyword_info = get_keyword_info(file_text, keyword)
        report_keyword_info.append('; '.join([str(info) for info in keyword_info]))
    output_df = pd.DataFrame(report_names, columns=['report_name'])
    output_df['keyword_info'] = report_keyword_info
    return output_df

output_df = get_keyword_information_from_report(folder_path, keyword = ['chemo', 'residual', 'nact'])

output_df.to_excel('D:\\Shweta\\path_reports\\output_df_sx_path_reports\\2021_03_08_chemo_info_from_pdf_reports.xlsx',
                   index=False)

output_df.to_excel('D:\\Shweta\\path_reports\\output_df_sx_path_reports\\2021_02_08_chemo_residual_info_from_pdf_reports.xlsx',
                   index=False)


# name_initials = ['mr', 'mrs', 'ms', 'miss']

