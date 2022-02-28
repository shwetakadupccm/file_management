import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process
import re
import dateparser

ffpe_data = pd.read_excel('D:/Shweta/Blocks_updated_data/2021_09_29_ffpe_data/2021_10_14_ffpe_all_1_1077_sk.xlsx')

cyto_df = pd.read_excel('D:/Shweta/path_reports/all_biopsy/extracted_data/2022_02_03_bx_cyto_histo_ihc_ki67_data_sk.xlsx',
                        sheet_name= 'cytology')

histo_df = pd.read_excel('D:/Shweta/path_reports/all_biopsy/extracted_data/2022_02_03_bx_cyto_histo_ihc_ki67_data_sk.xlsx',
                        sheet_name= 'histology')

ihc_df = pd.read_excel('D:/Shweta/path_reports/all_biopsy/extracted_data/2022_02_03_bx_cyto_histo_ihc_ki67_data_sk.xlsx',
                        sheet_name= 'immunohistochemistry')

##
cyto_merged = pd.merge(ffpe_data, cyto_df, how='inner', left_on='Lab_ID_SID', right_on='lab_sid')
cyto_filtered = cyto_merged[cyto_merged['Lab_ID_SID'].notnull()]
histo_merged = pd.merge(ffpe_data, histo_df, how='inner', left_on='Lab_ID_SID', right_on='lab_sid')
histo_filtered = histo_merged[histo_merged['Lab_ID_SID'].notnull()]
ihc_merged = pd.merge(ffpe_data, ihc_df, how='inner', left_on='IHC_biopsy_lab_id', right_on='lab_sid')
ihc_filtered = ihc_merged[ihc_merged['IHC_biopsy_lab_id'].notnull()]

writer = pd.ExcelWriter('D:/Shweta/path_reports/all_biopsy/merged_data/2022_02_04_merged_data_sk.xlsx',
                        engine='xlsxwriter')

cyto_filtered.to_excel(writer, sheet_name='cytology', index=False)
histo_filtered.to_excel(writer, sheet_name='histology', index=False)
ihc_filtered.to_excel(writer, sheet_name='immunohistochemistry', index=False)
writer.save()

def clean_names(df, name_str):
    cleaned_names = []
    for name in df[name_str]:
        name = re.sub('[^a-zA-Z]', ' ', str(name))
        name = name.lower()
        cleaned_names.append(name)
    return cleaned_names

def convert_all_dates_into_one_format(dates):
    dts = []
    for date in dates:
        dt_find = dateparser.parse(str(date))
        match = re.search('\d{4}-\d{2}-\d{2}', str(dt_find))
        if match is not None:
            dts.append(match[0])
        else:
            dts.append(date)
    return dts

def find_tils_score_from_ffpe(source_file, test_file, source_name_str='patient_name', source_sx_dt_str = 'sx_date',
                              source_tils_str = 'sx_tils', test_name_str='patient_name', test_sx_dt_str = 'sc_date',
                              test_tils_str = 'tils_score'):
    source_clean_names = clean_names(source_file, source_name_str)
    test_clean_names = clean_names(test_file, test_name_str)
    source_file['source_clean_dts'] = convert_all_dates_into_one_format(source_file[source_sx_dt_str])
    test_file['test_clean_dts'] = convert_all_dates_into_one_format(test_file[test_sx_dt_str])
    matched_list = []
    for index, name in enumerate(test_clean_names):
        matched_name = process.extractOne(query=name, choices=source_clean_names,
                                           scorer=fuzz.token_set_ratio)
        if matched_name is not None:
            test_cols = [test_name_str, test_tils_str, 'test_clean_dts']
            test_dat = test_file.iloc[index][test_cols]
            source_cols = [source_name_str, source_tils_str, 'source_clean_dts']
            source_index = source_clean_names.index(matched_name[0])
            source_dat = source_file.iloc[source_index][source_cols]
            score = matched_name[1]
            output_dat = np.append(test_dat, source_dat)
            final_output_list = np.append(output_dat, score)
            matched_list.append(final_output_list)
            matched_df = pd.DataFrame(matched_list, columns=[test_name_str, test_tils_str, 'test_sx_dates', source_name_str,
                                                             'ffpe_tils', 'ffpe_sx_dates', 'score'])

            # matched_df['comparison'] = np.where(matched_df['test_sx_dates'] == matched_df['ffpe_sx_dates'], True, False)
    return matched_df

matched_df = find_tils_score_from_ffpe(ffpe_data, path_df, source_name_str='patient_name', source_sx_dt_str = 'sx_date',
                              source_tils_str = 'sx_tils', test_name_str='patient_name', test_sx_dt_str = 'sc_date',
                              test_tils_str = 'tils_score')

matched_df['date_comparison'] = np.where(matched_df['test_sx_dates'] == matched_df['ffpe_sx_dates'], True, False)

matched_df.to_excel('D:\\Shweta\\path_reports\\2021_03_08_tils_ffpe_path_sk.xlsx', index=False)
##

def convert_float_into_percentage(tils):
    try:
        til_score = float(tils)
        til_score_float = (til_score * 100)
        til_score_percent = int(til_score_float)
        til_score_final = str(til_score_percent) + '%'
        return til_score_final
    except ValueError:
        return None


def cleaning_ffpe_tils_from_matched_with_text_mining(matched_df, ffpe_tils_str = 'sx_tils',
                                                     operators = ['<', '>']):
    cleaned_ffpe_tils = []
    for tils in matched_df[ffpe_tils_str]:
        til_score = convert_float_into_percentage(tils)
        if til_score is not None:
            cleaned_ffpe_tils.append(til_score)
        elif any(x in tils for x in operators):
            til_score = re.sub(r'([^<|>0-9%])', '', str(tils))
            cleaned_ffpe_tils.append(til_score)
        else:
            cleaned_ffpe_tils.append('data_not_available')
    matched_df['cleaned_ffpe_tils'] = cleaned_ffpe_tils
    return matched_df

matched_df1 = cleaning_ffpe_tils_from_matched_with_text_mining(matched_df, ffpe_tils_str = 'ffpe_tils',
                                                     operators = ['<', '>', '%'])

til_score = convert_float_into_percentage(str(0.2))