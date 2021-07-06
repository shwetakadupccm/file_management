import os
import pandas as pd
import shutil

file = open('D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt\\ANIL_DEVGAN_[_fnac].txt', 'r')

file_text = file.read()



file.read(8)

file.readlines()





##

folder_path = 'D:\\Shweta\\path_reports\\Jehangir_Surgery_Path_Reports\\2021_06_07_Jehangir_path_reports_txt'
destination_path = 'D:\\Shweta\\path_reports\\chemo_path_reports'

def read_file_text(folder_path, destination_path, string = 'chemotherapy'):
    file_names = os.listdir(folder_path)
    reports_name = []
    for file_name in file_names:
        file = open(folder_path + '\\' + file_name, 'r')
        file_text = file.read()
        file_text.lower()
        # print(file_text)
        source_path = os.path.join(folder_path, file_name)
        if string in file_text:
            print('string_is_there')
            reports_name.append(file_name)
            shutil.copy(source_path, destination_path)
        else:
            print('string_is_not_there')
    output_df = pd.DataFrame(reports_name, columns=['report_name'])
    return output_df

reports_name_chemo = read_file_text(folder_path, destination_path, string = 'chemotherapy')
# reports_name_chemo.to_excel('D:\\Shweta\\path_reports\\2021_07_06_chemotherapy_reports_names_sk.xlsx', index=False)

## nact

reports_name_nact = read_file_text(folder_path, string = 'nact')

##

reports_name_hormone_therapy = read_file_text(folder_path, string = 'hormone therapy')

##

reports_name_treatment = read_file_text(folder_path, string = 'treatment')

##

reports_name_fibrosis = read_file_text(folder_path, destination_path = 'D:\\Shweta\\path_reports\\2021_06_07_fibrosis_path_reports_sk', string = 'fibrosis')
reports_name_fibrosis.to_excel('D:\\Shweta\\path_reports\\2021_07_06_fibrosis_reports_names_sk.xlsx', index=False)
