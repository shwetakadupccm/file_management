import pandas as pd
from fpdf import FPDF

trial_file = pd.read_excel('D:\\Shweta\\surgery_images_ss\\trial_files_sk\\2021_08_11_trial_data_for_pdf_sk.xlsx')

def create_pdf_file_of_trail_data(trial_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    for i in range(16):
        print(i)
        file_number = trial_file['file_number'][i]
        print(file_number)
        pdf.cell(200, 10, txt='file_number = ' + str(file_number), ln=1, align='C')
        patient_name = trial_file['patient_name'][i]
        print(patient_name)
        pdf.cell(200, 10, txt='patient_name = ' + patient_name, ln=2, align='C')
        surgery_type_1 = trial_file['surgery_type_1'][i]
        print(surgery_type_1)
        pdf.cell(200, 10, txt='surgery_type_1 = ' + surgery_type_1, ln=3, align='C')
        surgery_type_2 = trial_file['surgery_type_2'][i]
        print(surgery_type_2)
        pdf.cell(200, 10, txt='surgery_type_2 = ' + surgery_type_2, ln=4, align='C')
        nact_yes_no = trial_file['nact_Yes_No'][i]
        print(nact_yes_no)
        pdf.cell(200, 10, txt = 'nact_status = ' + nact_yes_no, ln=5, align='C')
        sx_time = trial_file['sx_time'][i]
        print(sx_time)
        pdf.cell(200, 10, txt='sx_time = ' + sx_time, ln=6, align='C')
        type_file = trial_file['type_file'][i]
        print(type_file)
        pdf.cell(200, 10, txt='type_file = ' + type_file, ln=7, align='C')
        sx_date = trial_file['sx_date'][i]
        print(sx_date)
        pdf.cell(200, 10, txt='sx_date = ' + sx_date, ln=8, align='C')
        date_of_file = trial_file['date_of_file'][i]
        print(date_of_file)
        pdf.cell(200, 10, txt='date_of_file = ' + date_of_file, ln=9, align='C')
        folder = trial_file['folder'][i]
        print(folder)
        pdf.cell(200, 10, txt='folder = ' + folder, ln=10, align='C')
        file_name = trial_file['repo_file_name'][i]
        print(file_name)
        pdf.output('D:\\Shweta\\surgery_images_ss\\trial_files_sk\\output_pdf\\' + file_name)

create_pdf_file_of_trail_data(trial_file)
