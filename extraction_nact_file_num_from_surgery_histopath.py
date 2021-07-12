import os
import pandas as pd
import re
import numpy as np
import shutil

histo_reports_path = 'Y:\\Clinical_Database\\Digitized_Files\\Histopath\\Surgery'

histo_reports = os.listdir(histo_reports_path)

nact_data = pd.read_excel('D:\\Shweta\\nact_data\\2021_07_02_final_data_NACT_RU_dk.xlsx')

def cleaned_histo_reports(histo_reports_path):
    histo_reports = os.listdir(histo_reports_path)
    cleaned_histo_reports_file_num = []
    old_names = []
    for report in histo_reports:
        old_names.append(report)
        # print(report)
        cleaned_report_name = re.sub('.pdf', '', report)
        cleaned_report_name =re.sub('.Sx', '', cleaned_report_name)
        print(len(cleaned_report_name))
        cleaned_report_name = cleaned_report_name.replace('_', '/')
        print(cleaned_report_name)
        cleaned_report_name = cleaned_report_name[0:6]
        if cleaned_report_name.endswith('/'):
            cleaned_histo_reports_file_num.append(cleaned_report_name[0:5])
        else:
            cleaned_histo_reports_file_num.append(cleaned_report_name)
        output_df = pd.DataFrame(cleaned_histo_reports_file_num, columns = ['new_name'])
        output_df['old_name'] = old_names
    return output_df

cleaned_histo_reports_file_num = cleaned_histo_reports(histo_reports_path)

def find_file_number_in_nact_data(nact_data, histo_file_nums, nact_file_no_str = 'file_number',
                                  histo_file_no_str = 'new_name', histo_old_file_name_str = 'old_name'):
    histo_file_numbers = histo_file_nums[histo_file_no_str].tolist()
    common_file_nums = []
    for file_num in nact_data[nact_file_no_str]:
        if file_num in histo_file_numbers:
            file_num_index = histo_file_numbers.index(file_num)
            file_old_name = histo_file_nums.iloc[file_num_index][histo_old_file_name_str]
            common_file_nums.append(np.append(file_num, file_old_name))
            print(file_num)
            output_df = pd.DataFrame(common_file_nums, columns=['common_file_number', 'old_file_name'])
    return output_df

common_file_nums = find_file_number_in_nact_data(nact_data, cleaned_histo_reports_file_num, nact_file_no_str = 'file_number', histo_file_no_str = 'new_name')

for file in common_file_nums['old_file_name']:
    source_path = 'Y:\\Clinical_Database\\Digitized_Files\\Histopath\\Surgery'
    destination_path = 'D:\\Shweta\\path_reports\\2021_12_07_surgery_path_reports_nact_sk'
    shutil.copy(os.path.join(source_path, file), destination_path)

