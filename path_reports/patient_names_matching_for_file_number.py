import pandas as pd
import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import numpy as np

## Jeh data
ffpe_data = pd.read_excel('D:/Shweta/email/attachments_from_jehangir/jeh_reports_page_img_txt/output_df/matching_for_file_number/source_data/2021_09_23_ffpe_1_1050_patient_names_file_num_sx_date.xlsx')
jeh_sx_path_data = pd.read_excel('D:/Shweta/email/attachments_from_jehangir/jeh_reports_page_img_txt/output_df/matching_for_file_number/source_data/2021_09_23_jeh_sx_path_data_sk.xlsx')
sx_master = pd.read_excel('D:/Shweta/email/attachments_from_jehangir/jeh_reports_page_img_txt/output_df/matching_for_file_number/source_data/1179 Breast Sx Cases 2010 Till 2020  - Updated 19-01-2021   Sheet.xlsx',
                          sheet_name='Sheet1')
patient_master = pd.read_excel('D:/Shweta/Patient_name_matching/master_list/2010_2020_name_file_number_whole.xlsx')

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', ' ', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names

def find_file_num_from_master_list(source_file, test_file, source_name_str='Patient Name', source_file_str = 'file_number',
                                   test_name_str='patient_name'):
    source_clean_names = clean_names(source_file, source_name_str)
    test_clean_names = clean_names(test_file, test_name_str)
    matched_list = []
    for index, name in enumerate(test_clean_names):
        matched_name = process.extractOne(query=name, choices=source_clean_names,
                                           scorer=fuzz.token_set_ratio)
        if matched_name is not None:
            test_cols = [test_name_str]
            test_dat = test_file.iloc[index][test_cols]
            source_cols = [source_name_str, source_file_str]
            source_index = source_clean_names.index(matched_name[0])
            source_dat = source_file.iloc[source_index][source_cols]
            score = matched_name[1]
            output_dat = np.append(test_dat, source_dat)
            final_output_list = np.append(output_dat, score)
            matched_list.append(final_output_list)
            matched_df = pd.DataFrame(matched_list, columns=[test_name_str, source_name_str,
                                                             source_file_str, 'score'])
            #matched_df['comparison'] = np.where(matched_df[test_dt_str] == matched_df[surgery_dt_str], True, False)
    return matched_df

matched_df = find_file_num_from_master_list(patient_master, jeh_sx_path_data, source_name_str='patient_name', source_file_str = 'file_number',
                                   test_name_str='patient_name')

matched_df.to_excel('D:/Shweta/email/attachments_from_jehangir/jeh_reports_page_img_txt/output_df/matching_for_file_number/output_df/2021_09_23_matched_reports_names_file_number_from_master_list_sk.xlsx',
                    index=False)

## AG data

cyto_data = pd.read_excel('D:/Shweta/path_reports/AG_output_df/2021_09_22_bx_cyto_ihc_ki67_data_with_patient_name_file_number_sk.xlsx',
                     sheet_name='cyto_lab')

histo_df = pd.read_excel('D:/Shweta/path_reports/AG_output_df/2021_09_22_bx_cyto_ihc_ki67_data_with_patient_name_file_number_sk.xlsx',
                     sheet_name='histo_lab')

ihc_df = pd.read_excel('D:/Shweta/path_reports/AG_output_df/2021_09_22_bx_cyto_ihc_ki67_data_with_patient_name_file_number_sk.xlsx',
                     sheet_name='ihc_lab')

## cyto
cyto_ffpe = find_file_num_from_master_list(ffpe_data, cyto_data, source_name_str='Patient Name', source_file_str = 'file_number',
                                   test_name_str='patient_name')

cyto_master = find_file_num_from_master_list(patient_master, cyto_data, source_name_str='patient_name', source_file_str = 'file_number',
                                   test_name_str='patient_name')

## histo
histo_ffpe = find_file_num_from_master_list(ffpe_data, histo_df, source_name_str='Patient Name', source_file_str = 'file_number',
                                   test_name_str='patient_name')

histo_master = find_file_num_from_master_list(patient_master, histo_df, source_name_str='patient_name', source_file_str = 'file_number',
                                   test_name_str='patient_name')

##
ihc_ffpe = find_file_num_from_master_list(ffpe_data, ihc_df, source_name_str='Patient Name', source_file_str = 'file_number',
                                   test_name_str='patient_name')

ihc_master = find_file_num_from_master_list(patient_master, ihc_df, source_name_str='patient_name', source_file_str = 'file_number',
                                   test_name_str='patient_name')

##
writer = pd.ExcelWriter('D:/Shweta/path_reports/AG_output_df/matched_patient_names_for_file_num/2021_09_24_matched_names_for_reports_sk.xlsx',
                        engine='xlsxwriter')

cyto_ffpe.to_excel(writer, sheet_name='cytology_ffpe', index=False)
cyto_master.to_excel(writer, sheet_name='cytology_master', index=False)
histo_ffpe.to_excel(writer, sheet_name='histology_ffpe', index=False)
histo_master.to_excel(writer, sheet_name='histology_master', index=False)
ihc_ffpe.to_excel(writer, sheet_name='immunohistochemistry_ffpe', index=False)
ihc_master.to_excel(writer, sheet_name='immunohistochemistry_master', index=False)
writer.save()

## ruby hall sx data

ruby_data = pd.read_excel('D:/Shweta/email/attachments_from_ruby_hall/txt_img/output_df/2021_09_29_ruby_hall_sx_data_sk.xlsx')

ruby_ffpe = find_file_num_from_master_list(ffpe_data, ruby_data, source_name_str='Patient Name', source_file_str = 'file_number',
                                 test_name_str='patient_name')

ruby_sx = find_file_num_from_master_list(sx_master, ruby_data, source_name_str='Name ', source_file_str = 'File_number',
                                 test_name_str='patient_name')

ruby_master = find_file_num_from_master_list(patient_master, ruby_data, source_name_str='patient_name', source_file_str = 'file_number',
                                   test_name_str='patient_name')

writer = pd.ExcelWriter('D:/Shweta/email/attachments_from_ruby_hall/txt_img/output_df/matching_for_file_number/2021_09_24_matched_names_for_reports_sk.xlsx',
                        engine='xlsxwriter')

ruby_ffpe.to_excel(writer, sheet_name='from_ffpe', index=False)
ruby_sx.to_excel(writer, sheet_name='from_sx', index=False)
ruby_master.to_excel(writer, sheet_name='from_master', index=False)
writer.save()



