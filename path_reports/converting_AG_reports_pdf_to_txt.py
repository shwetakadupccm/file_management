import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import os

folder_path = 'D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy'

def convert_pdf_to_text(folder_path, output_file_path):
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        if file_name.endswith('.pdf'):
            file = open(os.path.join(folder_path, file_name), 'rb')
            rsrcmgr = PDFResourceManager()
            retstr = io.StringIO()
            # codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            page_no = 0
            for pageNumber, page in enumerate(PDFPage.get_pages(file)):
                if pageNumber == page_no:
                    interpreter.process_page(page)

                    data = retstr.getvalue()
                    cleaned_file_name = re.sub('.pdf', '', file_name)
                    new_file_name = cleaned_file_name + '_' + f'page_{page_no}.txt'
                    with open(os.path.join(output_file_path, new_file_name), 'wb') as file:
                        file.write(data.encode('utf-8'))
                    data = ''
                    retstr.truncate(0)
                    retstr.seek(0)

                page_no += 1

output_folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_txt_files'

convert_pdf_to_text(folder_path, output_folder_path)

##


import pytesseract as pt
from PIL import Image
from pdf2image import convert_from_path
pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


def convert_pdf_to_img_then_txt(pdf_folder_path, jpg_folder_path):
    pdf_files = os.listdir(pdf_folder_path)

    for pdf_file in pdf_files:
        if pdf_file.endswith('.pdf'):
            pages = convert_from_path(os.path.join(pdf_folder_path, pdf_file), 500,
                                      poppler_path = 'C:/Program Files/poppler-0.68.0/bin')
            i = 0
            for index, page in enumerate(pages):
                print(page)
                print(index)
                if i == index:
                    file_name = pdf_file.lower()
                    file_name = re.sub('.pdf', '', file_name)
                    out_jpg = file_name + '_' + str(i) + '.jpg'
                    page.save(os.path.join(jpg_folder_path, out_jpg), 'JPEG')
                    print(out_jpg)
                    img = Image.open(os.path.join(jpg_folder_path, out_jpg))
                    text = pt.image_to_string(img, lang="eng")
                    txt_file_path = os.path.join(jpg_folder_path, out_jpg + ".txt")
                    # print(text)
                    file1 = open(txt_file_path, "w")
                    file1.write(text)
                    file1.close()
                i += 1

convert_pdf_to_img_then_txt(folder_path, 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_txt_files_by_img/test_folder')
