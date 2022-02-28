import pandas as pd
# from PyPDF2 import PdfFileReader
import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pytesseract as pt
# from PIL import Image
from pdf2image import convert_from_path
import re
pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# file_path = 'D:/Shweta/data_digitization/scanned_patient_files/15_19.PDF'
dummy_img = 'D:/Shweta/data_digitization/reference_docs/PCCM_logo.png'
report_names_df = pd.read_excel('D:/Shweta/data_digitization/reference_docs/Report_types_17.xlsx',
                                sheet_name='report_types')
master_list = pd.read_excel('D:/Shweta/data_digitization/reference_docs/Report_types_17.xlsx',
                            sheet_name='master_list')
destination_path = 'D:/Shweta/data_digitization/trial_adding_logo'

## adding qr code

def add_qr_code_in_word_doc(report_type_df_path, qr_code_path, destination_path):
    for index, report_type in enumerate(report_type_df_path['report_types']):
        report_type_no = index + 1
        doc = Document()
        doc.add_picture(qr_code_path)
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        type = report_type
        text = doc.add_paragraph()
        report_type_name = text.add_run(str(report_type_no) + '. ' + type)
        report_type_name.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        report_type_name.bold = True
        report_type_name.font.size = Pt(28)
        report_type_name.font.name = 'Arial Black'
        doc.save(os.path.join(destination_path, report_type + '.docx'))

def add_id_info_in_word_doc(source_path, master_list, destination_path):
    for file in os.listdir(source_path):
        doc = Document(os.path.join(source_path, file))
        for i in range(len(master_list)):
            file_no = 'File_number: ' + str(master_list['file_number'][i])
            mr_no = 'MR_number: ' + str(master_list['mr_number'][i])
            patient_name = 'Patient_name: ' + str(master_list['patient_name'][i])
            dob = 'Date_of_Birth: ' + str(master_list['date_of_birth'][i])
            blank_para = doc.add_paragraph()
            run = blank_para.add_run()
            run.add_break()
            # id = doc.add_paragraph()
            id = doc.add_paragraph().add_run(file_no)
            id.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            id.font.size = Pt(20)
            id.font.name = 'Arial Black'
            id = doc.add_paragraph().add_run(mr_no)
            id.font.size = Pt(20)
            id.font.name = 'Arial Black'
            id = doc.add_paragraph().add_run(patient_name)
            id.font.size = Pt(20)
            id.font.name = 'Arial Black'
            id = doc.add_paragraph().add_run(dob)
            id.font.size = Pt(20)
            id.font.name = 'Arial Black'
            doc.save(os.path.join(destination_path, file))

add_id_info_in_word_doc('D:/Shweta/data_digitization/trial_adding_logo/added_images',
                            master_list,
                        'D:/Shweta/data_digitization/trial_adding_logo/added_id_info')

add_qr_code_in_word_doc(report_names_df, dummy_img, destination_path)

## converting pdf to jpg image

def convert_pdf_to_img(pdf_folder_path, jpg_folder_path):
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
                i += 1

# convert_pdf_to_img('D:/Shweta/data_digitization/scanned_patient_files/original_pdf',
#                    'D:/Shweta/data_digitization/scanned_patient_files/spplitted_pdf_to_img/15_19')

doc = Document()
document = doc.add_paragraph()
document.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
document.add_run('abc')
doc.save(os.path.join('D:/Shweta/data_digitization/trial_adding_logo/alignment', 'trial.docx'))

##
# doc = Document()
# qr_code = doc.add_picture(dummy_img)
# last_paragraph = doc.paragraphs[-1]
# last_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
# doc.save(os.path.join('D:/Shweta/data_digitization/trial_adding_logo/alignment', 'trial_img.docx'))
