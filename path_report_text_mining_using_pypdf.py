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

    for page in PDFPage.get_pages(file, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    file.close()
    device.close()
    retstr.close()
    return text

text = convert_pdf_to_txt(file_path)

np.savetxt('D:\\Shweta\\path_reports\\output_df_sx_path_reports\\2021_17_07_text.txt', text, fmt='%s')
string = 'chemotherapy'

text1 = text.replace('\n', '/')
text1 = text.replace(':', '/')
text1 = re.split('/', text1)
text_df = pd.DataFrame(text1, columns = ['report_text'])
text_df.to_excel('D:\\Shweta\\path_reports\\output_df_sx_path_reports\\2021_17_07_text_df_sx_path_report.xlsx')

name_initials = ['mr', 'mrs', 'ms', 'miss']

for line in text1:
    line = line.lower()
    # print(line)
    if any(x in line for x in name_initials):
        print(line)
    else:
        print('not_found')

str1 = 'CLINICAL DETAILS'
for line in text1:
    if str1 in line:
        print(line)
    else:
        print('not_found')

##
