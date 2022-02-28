import pandas as pd
import re
from fuzzywuzzy import process, fuzz
import numpy as np

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', ' ', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names

def find_file_num_from_master(source_file, test_file, source_name_str = 'Patient Names', source_file_str = 'file_number',
                                   test_name_str='patient_name'):
    source_clean_names = clean_names(source_file, source_name_str)
    test_clean_names = clean_names(test_file, test_name_str)
    matched_list = []
    for index, name in enumerate(test_clean_names):
        matched_name = process.extractOne(query=name, choices=source_clean_names,
                                           scorer=fuzz.token_set_ratio)
        print(matched_name)
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
    return matched_df

def get_mr_no_and_file_no_using_name(source_file, test_file, source_name_str = 'Patient Names', source_file_str = 'file_number',
                                   test_name_str='patient_name', test_file_str = 'file_number', source_mr_no_str = 'MR No'):
    source_clean_names = clean_names(source_file, source_name_str)
    test_clean_names = clean_names(test_file, test_name_str)
    matched_list = []
    score_lst = []
    for index, name in enumerate(test_clean_names):
        matched_name = process.extractOne(query=name, choices=source_clean_names,
                                           scorer=fuzz.token_set_ratio)
        print(matched_name)
        if matched_name is not None:
            test_cols = [test_name_str, test_file_str]
            test_dat = test_file.iloc[index][test_cols]
            source_cols = [source_name_str, source_file_str, source_mr_no_str]
            source_index = source_clean_names.index(matched_name[0])
            source_dat = source_file.iloc[source_index][source_cols]
            score = matched_name[1]
            score_lst.append(score)
            output_dat = np.append(source_dat, test_dat)
            print(output_dat)
            matched_list.append(output_dat)
    matched_df = pd.DataFrame(matched_list, columns=[source_name_str, source_file_str,
                                                     source_mr_no_str, test_name_str, test_file_str])
    matched_df['score'] = score_lst
    return matched_df

matched_df.to_excel('D:/Shweta/patient_lists/data_uploaded_on_server/matched_df/2021_01_06_matched_df_name_file_no_mr_no_sk.xlsx',
                    index=False)
