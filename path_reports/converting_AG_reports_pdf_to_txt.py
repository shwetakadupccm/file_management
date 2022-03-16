import re
import cv2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import os

# folder_path = 'D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy'

# def convert_pdf_to_text(folder_path, output_file_path):
#     file_names = os.listdir(folder_path)
#     for file_name in file_names:
#         if file_name.endswith('.pdf'):
#             file = open(os.path.join(folder_path, file_name), 'rb')
#             rsrcmgr = PDFResourceManager()
#             retstr = io.StringIO()
#             # codec = 'utf-8'
#             laparams = LAParams()
#             device = TextConverter(rsrcmgr, retstr, laparams=laparams)
#             interpreter = PDFPageInterpreter(rsrcmgr, device)
#
#             page_no = 0
#             for pageNumber, page in enumerate(PDFPage.get_pages(file)):
#                 if pageNumber == page_no:
#                     interpreter.process_page(page)
#
#                     data = retstr.getvalue()
#                     cleaned_file_name = re.sub('.pdf', '', file_name)
#                     new_file_name = cleaned_file_name + '_' + f'page_{page_no}.txt'
#                     with open(os.path.join(output_file_path, new_file_name), 'wb') as file:
#                         file.write(data.encode('utf-8'))
#                     data = ''
#                     retstr.truncate(0)
#                     retstr.seek(0)
#
#                 page_no += 1
#
# output_folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_txt_files'
#
# convert_pdf_to_text(folder_path, output_folder_path)

##
import pytesseract as pt
from PIL import Image
from pdf2image import convert_from_path
import ftfy
pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def convert_pdf_to_img_then_txt(pdf_folder_path, jpg_folder_path):
    pdf_files = os.listdir(pdf_folder_path)
    for pdf_file in pdf_files:
        print(pdf_file)
        pdf_file = pdf_file.lower()
        if pdf_file.endswith('.pdf'):
            pages = convert_from_path(os.path.join(pdf_folder_path, pdf_file), 500,
                                      poppler_path = 'C:/Program Files/poppler-0.68.0/bin')
            i = 0
            for index, page in enumerate(pages):
                if i == index:
                    file_name = pdf_file.lower()
                    file_name = re.sub('.pdf', '', file_name)
                    out_jpg = file_name + '_' + str(i) + '.jpg'
                    page.save(os.path.join(jpg_folder_path, out_jpg), 'JPEG')
                    img = Image.open(os.path.join(jpg_folder_path, out_jpg))
                    text = pt.image_to_string(img, lang="eng")
                    txt_file_name = re.sub('.jpg', '', out_jpg)
                    txt_file_path = os.path.join(jpg_folder_path, txt_file_name + ".txt")
                    # print(text)
                    file1 = open(txt_file_path, "w")
                    file1.write(text)
                    file1.close()
                i += 1

convert_pdf_to_img_then_txt("D:/Shweta/email/2022_03_03/AG/attchments",
                            "D:/Shweta/email/2022_03_03/AG/img_txt")

##
# file_name = '110_18_fnac_bx_ihc_2.jpg'
# folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_img_txt_files/trial_image_processing'

# img = Image.open(os.path.join(folder_path, file_name))
# width, height = img.size
# img = cv2.resize(img, (5000, 5000))
# text = pt.image_to_string(img, lang='eng')
#
# image = cv2.imread(os.path.join(folder_path, file_name))
# image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)[1]
# image = cv2.resize(image, (0, 0), fx=3, fy=3)
# image = cv2.medianBlur(image, 9)
# text1 = pt.image_to_string(image, lang='eng', config="--oem 3 --psm 11")
# text = ftfy.fix_text(text1)
# text = ftfy.fix_encoding(text)
# ##
# blurred = cv2.blur(image, (3,3))
# img = Image.fromarray(blurred)
# text2 = pt.image_to_string(image, lang='eng', config='--psm 0')
# print(text2)

##
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
# detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
# cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#
# for c in cnts:
#    cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
#
# repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 6))
# result = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_CLOSE, repair_kernel, iterations=1)
#
# text = pt.image_to_string(result, lang='eng', config='--psm 3')

def extract_text_from_image(folder_path, txt_file_folder_path):
    files = os.listdir(folder_path)
    for file in files:
        print(file)
        if file.endswith('.jpg'):
            image = cv2.imread(os.path.join(folder_path, file))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
            detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
            cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for c in cnts:
                cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

            repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 6))
            result = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_CLOSE, repair_kernel, iterations=1)

            text = pt.image_to_string(result, lang='eng', config='--psm 3')
            file_name = re.sub('.jpg', '', file)
            new_file_name = file_name + '.txt'
            txt_file_path = os.path.join(txt_file_folder_path, new_file_name)
            file1 = open(txt_file_path, "w")
            file1.write(text)
            file1.close()

txt_folder_path = "D:/Shweta/email/2022_03_03/AG/txt_files"
extract_text_from_image("D:/Shweta/email/2022_03_03/AG/img_txt",
                         txt_folder_path)

###
def convert_whole_pdf_to_img_then_txt(pdf_folder_path, jpg_folder_path):
    pdf_files = os.listdir(pdf_folder_path)
    for pdf_file in pdf_files:
        print(pdf_file)
        if pdf_file.endswith('.pdf'):
            pages = convert_from_path(os.path.join(pdf_folder_path, pdf_file), 500,
                                      poppler_path = 'C:/Program Files/poppler-0.68.0/bin')
            print(pages)
            # i = 0
            # for index, page in enumerate(pages):
            #     if i == index:
            file_name = pdf_file.lower()
            file_name = re.sub('.pdf', '', file_name)
            out_jpg = file_name + '_' + '.jpg'
            pages.save(os.path.join(jpg_folder_path, out_jpg), 'JPEG')
            print(out_jpg)
            img = Image.open(os.path.join(jpg_folder_path, out_jpg))
            text = pt.image_to_string(img, lang="eng")
            txt_file_name = re.sub('.jpg', '', out_jpg)
            txt_file_path = os.path.join(jpg_folder_path, txt_file_name + ".txt")
            # print(text)
            file1 = open(txt_file_path, "w")
            file1.write(text)
            file1.close()
            # i += 1

# convert_whole_pdf_to_img_then_txt('D:/Shweta/path_reports/Jehangir_Surgery_Path_Reports', 'D:/Shweta/email/attachments_from_jehangir/whole_report')


