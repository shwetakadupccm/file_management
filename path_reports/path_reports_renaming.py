import os
import pandas as pd
import re
import datetime
import shutil

# files = os.listdir(pdf_folder_path)
#
# for file in files:
#     created_date = time.ctime(os.path.getctime(os.path.join(pdf_folder_path, file)))
#     print("Created: %s" % time.ctime(os.path.getctime(os.path.join(pdf_folder_path, file))))
#     modified_date = time.ctime(os.path.getmtime(os.path.join(pdf_folder_path, file)))
#     print("Last modified: %s" % time.ctime(os.path.getmtime(os.path.join(pdf_folder_path, file))))

## renaming ag reports

def get_report_text_into_list(file_path):
    file = open(file_path, 'rt')
    lines = []
    for line in file:
        line_txt = line.strip(':, \n')
        if line_txt.isdigit():
            lines.append(line_txt)
        else:
            line_txt_cleaned = line_txt.lower()
            line_txt_cleaned = re.sub('reference:dr.koppikercb ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('reference', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.koppikercb', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('koppiker', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('sample collected at', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('orchids speciality breast care centre', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('flat no 1&2,', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('kapilvastu', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('sb road', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('next to ratna hospital', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('pune 411016 zone shiva', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('pune 411016zone shiva', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('pune 411016 zone', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('zone shiva', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('shva', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.c b ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.cb ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr. cb ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr. c b, ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('c b ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('cb ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('deshmukh chetan d md', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.deshmukh chetan d mbd', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('koprpiker cb ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('koppriker cb ms', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('dr.', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('accreditation asper iso certno mc refer scope wwwnablindiaorg', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('er/pr negative', '', line_txt_cleaned)
            line_txt_cleaned = re.sub('er/ppr negative', '', line_txt_cleaned)
            lines.append(line_txt_cleaned)
    file.close()
    return lines

def get_unique_value_from_list(list_with_duplicate_values):
    unique_list = []
    for value in list_with_duplicate_values:
        if value not in unique_list:
            unique_list.append(value)
    output_lst = [line for line in unique_list if line]
    return output_lst

def get_patient_name(text_lst):
    patient_name = text_lst[0]
    cleaned_patient_name = re.sub(r'[^a-zA-Z ]', '', str(patient_name))
    cleaned_patient_name = re.sub('sid', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('right side', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('right e', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('left e', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('lt e', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('rt e', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('right ref', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('ref', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('c b', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('msconsult antonco sur', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('report', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('cb ms', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('md', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('or ', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('right', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('left', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('breast', '', cleaned_patient_name)
    cleaned_patient_name = re.sub(' ms', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('msconsultantonco sur', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('msconsult antonco sur', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('case number', '', cleaned_patient_name)
    cleaned_patient_name = re.sub('consultantonco sur', '', cleaned_patient_name)
    cleaned_patient_name = cleaned_patient_name.strip()
    if cleaned_patient_name is not None:
        return cleaned_patient_name

def get_sid(text_lst, sid_keyword = 'sid'):
    for line in text_lst:
        if sid_keyword in line:
            sid = re.sub('\D', '', str(line))
            return sid

def get_sample_date(text_lst, sample_dt_keyword = 'sample date'):
    for line in text_lst:
        if sample_dt_keyword in line:
            sample_dt_index = text_lst.index(line)
            sample_dt = text_lst[sample_dt_index + 1]
            match = re.search('\d{2}-\d{2}-\d{4}', sample_dt)
            if match is not None:
                try:
                    date = datetime.datetime.strptime(match.group(), '%d-%m-%Y').date()
                    return date
                except ValueError:
                    return None

def make_hyperlink(path, file_name):
    url = "{}"
    return '=HYPERLINK("%s", "%s")' % (url.format(path), file_name)

def get_pdf_file_path(pdf_folder_path, file):
    file_name = file[:-6]
    pdf_file_name = file_name + '.pdf'
    file_path = os.path.join(pdf_folder_path, pdf_file_name)
    return pdf_file_name, file_path

def classify_report_by_type(text_lst, cytology_keyword = 'cytology report', histology_keyword = 'histology report',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum']):
    text_lst_str = str(text_lst)
    if cytology_keyword in text_lst_str:
        return 'cytology'
    elif histology_keyword in text_lst_str:
        return 'histology'
    elif ihc_keyword in text_lst_str:
        return 'immunohistochemistry'
    elif blood_count_keyword in text_lst_str:
        return 'complete_blood_count'
    elif ki_keyword in text_lst_str:
        return 'ki67'
    elif glucose_keyword in text_lst_str:
        return 'plasma_glucose'
    elif any(x in text_lst_str for x in nutrient_keyword):
        return 'nutrient_report'
    elif liver_keyword in text_lst_str:
        return 'liver_function_test'
    else:
        return 'type_not_found'

def get_identification_data(file_txt_unique, sample_dt_keyword = 'sample date', cytology_keyword = 'cytology report',
                            histology_keyword = 'histology report',  ihc_keyword = 'immunohistochemistry', sid_keyword = 'sid',
                            blood_count_keyword = 'blood count', ki_keyword = 'ki 67', glucose_keyword = 'glucose',
                            liver_keyword = 'liver', nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum']):
    patient_name = get_patient_name(file_txt_unique)
    sample_date = get_sample_date(file_txt_unique, sample_dt_keyword)
    sample_date = str(sample_date)
    sid = get_sid(file_txt_unique, sid_keyword)
    report_type = classify_report_by_type(file_txt_unique, cytology_keyword, histology_keyword, ihc_keyword, blood_count_keyword,
                                          ki_keyword, glucose_keyword, liver_keyword, nutrient_keyword)
    identification_data = [patient_name, sample_date, sid, report_type]
    return identification_data

def get_report_data_of_all_pages(txt_folder_path, pdf_folder_path, sample_dt_keyword = 'sample date',
                            cytology_keyword = 'cytology report', sid_keyword = 'sid',
                            histology_keyword = 'histology report',  ihc_keyword = 'immunohistochemistry',
                            blood_count_keyword = 'blood count', ki_keyword = 'ki 67', glucose_keyword = 'glucose',
                            liver_keyword = 'liver', nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum']):
    file_names = os.listdir(txt_folder_path)
    indentification_data_lst = []
    for file_name in file_names:
        if file_name.endswith('.txt'):
            print(file_name)
            pdf_file_name, pdf_file_path = get_pdf_file_path(pdf_folder_path, file_name)
            hyperlink = make_hyperlink(pdf_file_path, pdf_file_name)
            file_txt = get_report_text_into_list(os.path.join(txt_folder_path, file_name))
            file_txt_unique = get_unique_value_from_list(file_txt)
            identification_data = get_identification_data(file_txt_unique, sample_dt_keyword, cytology_keyword,
                            histology_keyword,  ihc_keyword, sid_keyword, blood_count_keyword, ki_keyword, glucose_keyword,
                            liver_keyword, nutrient_keyword)
            new_file_name = file_name[:-6]
            new_file_name = new_file_name + '.pdf'
            identification_data.insert(0, new_file_name)
            identification_data.insert(1, hyperlink)
            indentification_data_lst.append(identification_data)
    output_df = pd.DataFrame(indentification_data_lst, columns=['file_name', 'hyperlink', 'patient_name', 'sample_date', 'sid',
                                                                'report_type'])
    return output_df

txt_folder_path = 'D:/Shweta/email/2022_03_01/AG/txt_files'
pdf_folder_path = 'D:/Shweta/email/2022_03_01/AG/attachments'

output_df = get_report_data_of_all_pages(txt_folder_path, pdf_folder_path, sample_dt_keyword = 'sample date')

output_df.to_excel('D:/Shweta/email/2022_03_01/AG/renaming_df/2022_03_04_pdf_names_info.xlsx',
                   index=False)

df = pd.read_excel('D:/Shweta/email/2022_03_03/AG/renaming_df/2022_03_04_pdf_names_info.xlsx', sheet_name='renaming_data')

def make_new_file_name_for_ag_report(final_pdf_info_df):
    new_names = []
    for i in range(len(final_pdf_info_df)):
        patient_name = final_pdf_info_df.iloc[i]['patient_name']
        patient_name = patient_name.strip()
        patient_name = patient_name.replace(' ', '_')
        sample_date = final_pdf_info_df.iloc[i]['sample_date']
        # sample_date = sample_date.date()
        sample_date = re.sub('-', '_', str(sample_date))
        new_name = patient_name + '_' + sample_date + '.pdf'
        new_names.append(new_name)
    final_pdf_info_df['new_pdf_name'] = new_names
    return final_pdf_info_df

df = make_new_file_name_for_ag_report(df)

def make_new_file_name(final_pdf_info_df):
    new_names = []
    for i in range(len(final_pdf_info_df)):
        patient_name = final_pdf_info_df.iloc[i]['patient_name']
        patient_name = patient_name.replace(' ', '_')
        sample_date = final_pdf_info_df.iloc[i]['sc_date']
        sample_date = sample_date.date()
        sample_date = re.sub('-', '_', str(sample_date))
        type = final_pdf_info_df.iloc[i]['report_type']
        new_name = patient_name + '_' + sample_date + '_' + type + '.pdf'
        new_names.append(new_name)
    final_pdf_info_df['new_pdf_name'] = new_names
    return final_pdf_info_df

df = make_new_file_name(df)


df.to_excel('D:/Shweta/email/2022_03_03/AG/renaming_df/2022_03_04_pdf_names_info_new_names.xlsx',
            index=False)

## renaming golwilkar scanned reports

# def rename_pdf_file_name(pdf_folder_path, pdf_info_df, destination_pdf_path):
#     pdf_file_names = pdf_info_df['file_name']
#     pdf_file_new_names = pdf_info_df['new_pdf_name']
#     try:
#         for index, pdf_file_name in enumerate(pdf_file_names):
#             source_path = os.path.join(pdf_folder_path, pdf_file_name)
#             new_pdf_name = pdf_file_new_names[index]
#             shutil.copy(source_path, os.path.join(destination_pdf_path, new_pdf_name))
#             print('renamed_and_copied')
#     except FileNotFoundError:
#         print('file_not_found')

destination_path = 'D:/Shweta/email/2022_03_01/AG/renamed_reports'

def rename_pdf_file_name(pdf_folder_path, pdf_info_df, destination_pdf_path):
    pdf_file_names = pdf_info_df['file_name']
    pdf_file_new_names = pdf_info_df['new_pdf_name']
    for index, pdf_file_name in enumerate(pdf_file_names):
        source_path = os.path.join(pdf_folder_path, pdf_file_name)
        new_pdf_name = pdf_file_new_names[index]
        shutil.copy(source_path, os.path.join(destination_pdf_path, new_pdf_name))
        print('renamed_and_copied')

rename_pdf_file_name('D:/Shweta/path_reports/all_biopsy/biopsy_reports', df, destination_path)

def sort_pdf_year_wise_and_copy(renamed_pdf_folder_path, destination_pdf_path):
    pdf_files = os.listdir(renamed_pdf_folder_path)
    for pdf_file in pdf_files:
        if pdf_file.endswith('.pdf'):
            source_path = os.path.join(renamed_pdf_folder_path, pdf_file)
            match = re.search('\d{4}_\d{2}_\d{2}', pdf_file)
            if match is not None:
                dt = datetime.datetime.strptime(match.group(), '%Y_%m_%d').date().year
                dt_path = os.path.join(destination_pdf_path, str(dt))
                if not os.path.isdir(dt_path):
                    os.mkdir(dt_path)
                new_dest = os.path.join(dt_path, pdf_file)
                shutil.copy(source_path, new_dest)
                print('file_copied')

# sort_pdf_year_wise_and_copy('D:/Shweta/path_reports/all_biopsy/renamed_files',
#                             'D:/Shweta/path_reports/all_biopsy/sorted_year_wise')

def rename_pdf_file_name_by_patient_name_date(pdf_folder_path, pdf_info_df, destination_pdf_path):
    pdf_file_names = pdf_info_df['file_name']
    pdf_file_new_names = pdf_info_df['new_pdf_name']
    for index, pdf_file_name in enumerate(pdf_file_names):
        source_path = os.path.join(pdf_folder_path, pdf_file_name)
        new_pdf_name = pdf_file_new_names[index]
        match = re.search('\d{4}_\d{2}_\d{2}', new_pdf_name)
        if match is not None:
            dt = datetime.datetime.strptime(match.group(), '%Y_%m_%d').date().year
            dt_path = os.path.join(destination_pdf_path, str(dt))
            if not os.path.isdir(dt_path):
                os.mkdir(dt_path)
            new_dest = os.path.join(dt_path, new_pdf_name)
            shutil.copy(source_path, new_dest)
            print('file_renamed_and_copied')

destination_pdf_path = 'D:/Shweta/email/attachments_from_ag/date_wise_reports'

rename_pdf_file_name_by_patient_name_date(pdf_folder_path, output_df, destination_pdf_path)

