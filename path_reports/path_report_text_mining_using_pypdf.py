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

###

test_folder = 'D:/Shweta/path_reports/Histopath_reports_from_server/test_output'
import PyPDF2

pdf_file = open(os.path.join(img_path, img_name), 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)
count = pdf_reader.numPages

for i in range(count):
    page = pdf_reader.getPage(i)
    text = page.extractText()
    test_file_path = os.path.join(test_folder, 'trial_txt' + '_' + str(i) + '.txt')
    file1 = open(test_file_path, "w", encoding='utf-8')
    file1.write(text)
    file1.close()

##
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image

# pdfFile = os.path.join(path, pdfName)

inputpdf = PdfFileReader(open(file_path, "rb"))
for i in range(inputpdf.numPages):
    outputName = file_path[0:-4] + '_' + str(i) + '.jpg'
    output = Image.Image.convert()
    output.addPage(inputpdf.getPage(i))
    with open(outputName, "wb") as outputStream:
        output.write(outputStream)


##

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
import io
import os

test_folder = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_pdf_txt_not_extracted/test_folder'

fp = open(os.path.join(img_path, img_name), 'rb')
rsrcmgr = PDFResourceManager()
retstr = io.StringIO()
code = 'utf-8'
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

page_no = 0
for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
    if pageNumber == page_no:
        interpreter.process_page(page)

        data = retstr.getvalue()
        cleaned_file_name = re.sub('.pdf', '', img_name)
        new_file_name = cleaned_file_name + '_' + f'page_{page_no}.txt'
        with open(os.path.join(test_folder, new_file_name), 'wb') as file:
            file.write(data.encode('utf-8'))
        data = ''
        retstr.truncate(0)
        retstr.seek(0)

    page_no += 1

##
img_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_pdf_txt_not_extracted'
img_name = '06_13_Bx.PDF'

import pytesseract as pt
from PIL import Image
from pdf2image import convert_from_path

pdf_img = convert_from_path(os.path.join(img_path, img_name), 500, poppler_path = 'C:/Program Files/poppler-0.68.0/bin')

pages = convert_from_path(os.path.join(img_path, img_name), 500, poppler_path = 'C:/Program Files/poppler-0.68.0/bin')
out_jpg = img_name +'.jpg'

pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

for page in pages:
    page.save(os.path.join(test_folder, out_jpg), 'JPEG')
    print(out_jpg)
    img = Image.open(os.path.join(test_folder, out_jpg))
    text = pt.image_to_string(img, lang="eng")
    imageName = img_name
    fullTempPath = os.path.join(test_folder, img_name + ".txt")
    print(text)
    # saving the  text for every image in a separate .txt file
    file1 = open(fullTempPath, "w")
    file1.write(text)
    file1.close()






