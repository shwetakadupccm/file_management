import pytesseract as pt
from PIL import Image
from pdf2image import convert_from_path
import os
import re

pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def convert_pdf_to_img_then_txt(pdf_folder_path, jpg_folder_path):
    pdf_files = os.listdir(pdf_folder_path)
    for pdf_file in pdf_files:
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
                    print(out_jpg)
                    img = Image.open(os.path.join(jpg_folder_path, out_jpg))
                    text = pt.image_to_string(img, lang="eng")
                    txt_file_name = re.sub('.jpg', '', out_jpg)
                    txt_file_path = os.path.join(jpg_folder_path, txt_file_name + ".txt")
                    # print(text)
                    file1 = open(txt_file_path, "w")
                    file1.write(text)
                    file1.close()
                i += 1

convert_pdf_to_img_then_txt('D:/Shweta/email/attachments_from_ruby_hall', 'D:/Shweta/email/attachments_from_ruby_hall/txt_img')
