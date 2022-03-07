import os
import re
import pandas as pd
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx2pdf import convert
from fpdf import FPDF


class DataDigitization:

    def __init__(self, root):
        self.root = root
        self.report_names_df = pd.read_excel(
            os.path.join(self.root, 'reference_docs/Report_types_17.xlsx'), sheet_name='report_types')
        # make master_list a separate xls
        self.master_list = pd.read_excel(os.path.join(self.root, 'reference_docs/Report_types_17.xlsx'),
                                         sheet_name='master_list')
        self.coded_data = os.path.join(self.root, 'report_types_added_qr_code')
        self.qr_code_path = os.path.join(self.root, 'sample_from_HR/549_16')
        self.tmp = os.path.join(self.root, 'tmp')
        self.file = os.path.join(self.root, 'scanned_files')

    def add_qr_code_in_word_doc(self):
        for index, report_type in enumerate(self.report_names_df['report_types']):
            report_type_no = index + 1
            doc = Document()
            doc.add_picture(self.qr_code_path)
            last_paragraph = doc.paragraphs[-1]
            last_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            type = report_type
            text = doc.add_paragraph()
            report_type_name = text.add_run(str(report_type_no) + '. ' + type)
            report_type_name.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
            report_type_name.bold = True
            report_type_name.font.size = Pt(28)
            report_type_name.font.name = 'Arial Black'
            # doc.save(os.path.join(self.coded_data, report_type + '.docx'))
            for i in range(len(self.master_list)):
                file_no = 'File_number: ' + \
                    str(self.master_list['file_number'][i])
                file_number = str.replace(file_no, '/', '_')
                mr_no = 'MR_number: ' + str(self.master_list['mr_number'][i])
                patient_name = 'Patient_name: ' + \
                    str(self.master_list['patient_name'][i])
                dob = 'Date_of_Birth: ' + \
                    str(self.master_list['date_of_birth'][i])
                dir = self.master_list['file_number'][i]
                dir = re.sub('/', '_', str(dir))
                qr_label = os.path.join(self.coded_data, file_number)
                if not os.path.isdir(qr_label):
                    os.mkdir(qr_label)
                blank_para = doc.add_paragraph()
                run = blank_para.add_run()
                run.add_break()
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
                report_type = re.sub(' ', '_', report_type)
                report_type = report_type.lower()
                doc_name = str(report_type_no) + '_' + report_type + '.docx'
                doc.save(os.path.join(qr_label, doc_name))
                return qr_label

        # restart from here.
    def add_report_data(self, qr_label):
        reports = os.listdir(qr_label)
        for report in reports:
            print(report)
            report_name = re.sub('.docx', '', str(report))
            print(report_name)
            each_report_dir = (os.path.join(self.tmp), report_name)
            os.mkdir(each_report_dir)
            doc_path = os.path.join(self.tmp, report_name)
            print(doc_path)
            pdf_report_name = re.sub('[^0-9]', '', str(report_name))
            pdf_report_name = pdf_report_name + '_code.pdf'
            pdf_path = os.path.join(each_report_dir, pdf_report_name)
            convert(doc_path, pdf_path)
            self.create_dummy_images_for_reports(dir_name, each_report_dir)

    @staticmethod
    def create_dummy_images_for_reports(report_type, dir_path):
        for i in range(5):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', size=28)
            text_letter = re.sub('[^a-z_]', '', str(self.))
            print(text_letter)
            text = text_letter[1:] + '_' + str(i)
            pdf.cell(200, 10, txt=text, ln=1, align='C')
            report_type = re.sub('[^a-z_]', '', str(report_type))
            pdf_name = report_type[1:] + '_' + str(i) + '.pdf'
            pdf.output(os.path.join(dir_path, pdf_name))

    def extract_report_data_from_file(self):
        # scanned data either as images or as pdf
        # excel of categorised data - dk to send now
        