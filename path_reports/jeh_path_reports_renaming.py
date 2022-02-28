import pandas as pd
import os
import re
import datetime
import shutil

def get_report_text_into_list(file_path):
    file = open(file_path, 'rt')
    lines = []
    for line in file:
        line_txt = line.strip(':, \n')
        if line_txt.isdigit():
            lines.append(line_txt)
        else:
            line_txt_cleaned = line_txt.lower()
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

def get_patinet_name(report_text_lst, name_str = 'name'):
    for line in report_text_lst:
        if name_str in line:
            patient_name = re.sub('[^A-Za-z ]', '', str(line))
            patient_name = re.sub('name', '', patient_name)
            patient_name = re.sub('agesex', '', patient_name)
            patient_name = re.sub('yrs', '', patient_name)
            patient_name = re.sub('ytrs', '', patient_name)
            patient_name = re.sub('female', '', patient_name)
            patient_name = re.sub('male', '', patient_name)
            patient_name = re.sub('mrs', '', patient_name)
            patient_name = re.sub('ms', '', patient_name)
            patient_name = re.sub('mr', '', patient_name)
            patient_name = re.sub('miss', '', patient_name)
            patient_name = patient_name.strip()
            return patient_name

def get_tagged_date(report_text_lst, tag_str = 'sc date'):
    for line in report_text_lst:
        if tag_str in line:
            sc_date_name_index = report_text_lst.index(line)
            sc_date_txt = report_text_lst[sc_date_name_index]
            if sc_date_name_index is not None:
                try:
                    match = re.search('\d{2}/\d{2}/\d{4}', sc_date_txt)
                    date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
                    if date is not None:
                        return date
                except AttributeError:
                    return None

def get_jpg_file_path(folder_path, file):
    file_name = re.sub('.txt', '.jpg', file)
    file_path = os.path.join(folder_path, file_name)
    return file_name, file_path

def make_hyperlink(path, file_name):
    url = "{}"
    return '=HYPERLINK("%s", "%s")' % (url.format(path), file_name)

def get_report_data(txt_folder_path, name_str = 'name', tag_str = 'sc date'):
    file_names = os.listdir(txt_folder_path)
    report_data_extracted = []
    for file_name in file_names:
        if file_name.endswith('.txt'):
            print(file_name)
            file_txt = get_report_text_into_list(os.path.join(txt_folder_path, file_name))
            file_txt_unique = get_unique_value_from_list(file_txt)
            jpg_file_name, file_path = get_jpg_file_path(txt_folder_path, file_name)
            hyper_link = make_hyperlink(file_path, jpg_file_name)
            pdf_file_name = file_name[:-6]
            patient_name = get_patinet_name(file_txt_unique, name_str)
            sc_date = get_tagged_date(file_txt_unique, tag_str)
            data_extracted = [file_name, pdf_file_name, hyper_link, patient_name, sc_date]
            report_data_extracted.append(data_extracted)
    output_df = pd.DataFrame(report_data_extracted, columns=['report_name', 'pdf_file_name', 'hyperlink_of_jpg_file',
                                                             'patient_name', 'sc_date'])
    return output_df

df = get_report_data('D:/Shweta/email/attachments_from_jehangir/all_jehangir/img_txt', name_str = 'name', tag_str = 'sc date')
df.to_excel('D:/Shweta/email/attachments_from_jehangir/all_jehangir/output_df/2021_10_09_jeh_sx_data_for_renmaing_sk.xlsx',
            index=False)

df = pd.read_excel('D:/Shweta/email/attachments_from_jehangir/all_jehangir/output_df/2021_10_09_jeh_sx_data_for_renmaing_sk.xlsx')

def make_new_file_name(final_pdf_info_df):
    new_names = []
    for i in range(len(final_pdf_info_df)):
        patient_name = final_pdf_info_df.iloc[i]['patient_name']
        patient_name = patient_name.replace(' ', '_')
        sample_date = final_pdf_info_df.iloc[i]['sc_date']
        sample_date = sample_date.date()
        sample_date = re.sub('-', '_', str(sample_date))
        new_name = patient_name + '_' + sample_date + '.pdf'
        new_names.append(new_name)
    final_pdf_info_df['new_pdf_name'] = new_names
    return final_pdf_info_df

df = make_new_file_name(df)

def rename_pdf_file_name(pdf_folder_path, pdf_info_df, destination_pdf_path):
    pdf_file_names = pdf_info_df['pdf_file_name']
    pdf_file_new_names = pdf_info_df['new_pdf_name']
    for index, file_name in enumerate(pdf_file_names):
        source_path = os.path.join(pdf_folder_path, file_name + '.pdf')
        new_pdf_name = pdf_file_new_names[index]
        shutil.copy(source_path, os.path.join(destination_pdf_path, new_pdf_name))
        print('renamed_and_copied')

rename_pdf_file_name('D:/Shweta/email/attachments_from_jehangir/all_jehangir/pdf_files',
                     df, 'D:/Shweta/email/attachments_from_jehangir/all_jehangir/renamed_pdf')

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

sort_pdf_year_wise_and_copy('D:/Shweta/email/attachments_from_jehangir/all_jehangir/renamed_pdf',
                            'D:/Shweta/email/attachments_from_jehangir/all_jehangir/year_wise_report')
