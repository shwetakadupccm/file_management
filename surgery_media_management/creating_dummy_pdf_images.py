import pandas as pd
from fpdf import FPDF

trial_file = pd.read_excel('D:/Shweta/surgery_images_ss/trial_files_sk/2021_08_11_trial_data_for_pdf_sk.xlsx')
sample_data = pd.read_excel('D:/Shweta/surgery_images_ss/trial_files_sk/2021_08_21_Sample_data.xlsx')

def create_pdf_file_of_trial_data(trial_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    for i in range(len(trial_file)):
        file_number = trial_file['file_number'][i]
        pdf.cell(200, 10, txt='file_number = ' + str(file_number), ln=1, align='C')
        mr_number = trial_file['MR_NUMBER'][i]
        pdf.cell(200, 10, txt='mr_number = ' + str(mr_number), ln=2, align='C')
        patient_name = trial_file['patient_name'][i]
        pdf.cell(200, 10, txt='patient_name = ' + str(patient_name), ln=3, align='C')
        surgery_type_1 = trial_file['surgery_type_1'][i]
        pdf.cell(200, 10, txt='surgery_type_1 = ' + str(surgery_type_1), ln=4, align='C')
        surgery_type_2 = trial_file['surgery_type_2'][i]
        pdf.cell(200, 10, txt='surgery_type_2 = ' + str(surgery_type_2), ln=5, align='C')
        nact_yes_no = trial_file['nact_yes_no'][i]
        pdf.cell(200, 10, txt = 'nact_status = ' + str(nact_yes_no), ln=6, align='C')
        sx_time = trial_file['sx_time_period'][i]
        pdf.cell(200, 10, txt='sx_time_period = ' + str(sx_time), ln=7, align='C')
        sx_date = trial_file['sx_date'][i]
        pdf.cell(200, 10, txt='sx_date = ' + str(sx_date), ln=8, align='C')
        date_of_image_file = trial_file['date_of_image_file'][i]
        pdf.cell(200, 10, txt='date_of_image_file = ' + str(date_of_image_file), ln=9, align='C')
        nact_time_period = trial_file['nact_time_period'][i]
        pdf.cell(200, 10, txt='nact_time_period = ' + str(nact_time_period), ln=10, align='C')
        type_file = trial_file['type_file'][i]
        pdf.cell(200, 10, txt='type_file = ' + str(type_file), ln=11, align='C')
        file_name = trial_file['repo_file_name'][i]
        if type_file == 'Image':
            pdf.output('D:/Shweta/surgery_images_ss/trial_files_sk/2021_08_21_output_pdf_of_sample_data_by_type/Image/' + file_name + '.pdf')
        elif type_file == 'Video':
            pdf.output('D:/Shweta/surgery_images_ss/trial_files_sk/2021_08_21_output_pdf_of_sample_data_by_type/Video/' + file_name + '.pdf')
        elif type_file == 'Specimen':
            pdf.output('D:/Shweta/surgery_images_ss/trial_files_sk/2021_08_21_output_pdf_of_sample_data_by_type/Specimen/' + file_name + '.pdf')

create_pdf_file_of_trial_data(sample_data)

def create_dummy_pdf_file_for_each_type(trial_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    for i in range(len(trial_file)):
        file_number = trial_file['file_number'][i]
        pdf.cell(200, 10, txt='file_number = ' + str(file_number), ln=1, align='C')
        mr_number = trial_file['MR_NUMBER'][i]
        pdf.cell(200, 10, txt='mr_number = ' + str(mr_number), ln=2, align='C')
        patient_name = trial_file['patient_name'][i]
        pdf.cell(200, 10, txt='patient_name = ' + str(patient_name), ln=3, align='C')
        surgery_type_1 = trial_file['surgery_type_1'][i]
        pdf.cell(200, 10, txt='surgery_type_1 = ' + str(surgery_type_1), ln=4, align='C')
        surgery_type_2 = trial_file['surgery_type_2'][i]
        pdf.cell(200, 10, txt='surgery_type_2 = ' + str(surgery_type_2), ln=5, align='C')
        nact_yes_no = trial_file['nact_yes_no'][i]
        pdf.cell(200, 10, txt = 'nact_status = ' + str(nact_yes_no), ln=6, align='C')
        sx_time = trial_file['sx_time_period'][i]
        pdf.cell(200, 10, txt='sx_time_period = ' + str(sx_time), ln=7, align='C')
        sx_date = trial_file['sx_date'][i]
        pdf.cell(200, 10, txt='sx_date = ' + str(sx_date), ln=8, align='C')
        date_of_image_file = trial_file['date_of_image_file'][i]
        pdf.cell(200, 10, txt='date_of_image_file = ' + str(date_of_image_file), ln=9, align='C')
        nact_time_period = trial_file['nact_time_period'][i]
        pdf.cell(200, 10, txt='nact_time_period = ' + str(nact_time_period), ln=10, align='C')
        type_file_image = trial_file['file_type(image)'][i]
        if type_file_image == 'Image':
            # pdf.cell(200, 10, txt='type_file = ' + str(type_file_image), ln=11, align='C')
            file_name_image = trial_file['repo_file_name_for_image'][i]
            pdf.output('D:/Shweta/surgery_images_ss/trial_files_sk/2021_08_23_output_pdf_of_sample_data_by_type/Image/' + file_name_image + '.pdf')
        type_file_video = trial_file['file_type(Video)'][i]
        if type_file_video == 'Video':
            # pdf.cell(200, 10, txt='type_file = ' + str(type_file_video), ln=11, align='C')
            file_name_video = trial_file['repo_file_name_for_video'][i]
            pdf.output('D:/Shweta/surgery_images_ss/trial_files_sk/2021_08_23_output_pdf_of_sample_data_by_type/Video/' + file_name_video + '.pdf')
        type_file_specimen = trial_file['file_type(Specimen)'][i]
        if type_file_specimen == 'Specimen':
            # pdf.cell(200, 10, txt='type_file = ' + str(type_file_specimen), ln=11, align='C')
            file_name_specimen = trial_file['repo_file_name_for_video'][i]
            pdf.output('D:/Shweta/surgery_images_ss/trial_files_sk/2021_08_23_output_pdf_of_sample_data_by_type/Specimen/' + file_name_specimen + '.pdf')

create_dummy_pdf_file_for_each_type(sample_data)

