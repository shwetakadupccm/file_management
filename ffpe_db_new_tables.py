import pandas as pd
import numpy as np
import uuid
import os

# ffpe_db = pd.read_excel('D:\\Shweta\\Blocks_updated_data\\2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx')
# # # mapping  = pd.read_excel('D:\\Shweta\\Blocks_updated_data\\Final_R_code_excel_files\\2021_02_15_column_names_mapping_sk.xlsx')

TABLE_DICT = {'block_information': 'primary',
                'fnac': ['site', 'type'],
                'biopsy': ['site', 'type'],
                'biopsy_ihc': ['site', 'type'],
                'surgery': 'type',
                'surgery_ihc': 'type'}

table_types_site = {'type': ['primary', 'review'],
                    'site': ['breast', 'node','other']}

def generate_pk(df):
    pks = []
    for i in range(0, len(df)):
        pk = uuid.uuid4().hex
        pks.append(pk)
    return pks

def add_fk(df, key_col_name):
    df[key_col_name] = generate_pk(df)
    return df
# ffpe_db['pk'] = generate_pk(ffpe_db)
# cols = ffpe_db.columns.to_list()
# cols = cols[-1:] + cols[:-1]
# cols
# ffpe_db = ffpe_db[cols]

def get_input_data():
    folder = 'D:/WorkDocs/OneDrive/iiser_data/Prashanti_docs/Database_files/Block_data_biopsy_surgery//for db'
    ffpe_file = '2021_01_25_PCCM_FFPE_1_672.xlsx'
    mapping_file = '2021_02_13FFPE_column_names_mapping_sk.xlsx'
    ffpe_db_path = os.path.join(folder, ffpe_file)
    mapping_path = os.path.join(folder, mapping_file)
    ffpe_db = pd.read_excel(ffpe_db_path)
    mapping = pd.read_excel(mapping_path)
    ffpe_db = add_fk(ffpe_db, 'pk')
    return (ffpe_db, mapping)


def get_table_map(mapping, table):
    dat = mapping[['old_names', table]]
    filtered_df = dat[dat[table].notnull()]
    filtered_df = filtered_df.rename(columns = {table: 'table_tbd'})
    return filtered_df

# filtered_df = get_table_map(mapping,'block_information')

def get_old_col(filtered_df, new_col):
    new_col = (filtered_df[filtered_df.table_tbd == new_col])
    old_col = new_col['old_names'].to_list()[0]
    return old_col


# old_col = get_old_col(filtered_df, 'file_number')


def add_old_data_new_cols(df, map_df):
    df_all = pd.DataFrame(df['pk'])
    for col in map_df['table_tbd']:
        print(col)
        old_col = get_old_col(map_df, col)
        print(old_col)
        df_col = df_all
        try:
            df_col[col] = df[old_col]
        except KeyError:
            df_col[col] = ['data_not_curated'] * len(df)
        df_table = pd.merge(df_col, df_all, on='pk')
    return df_table


def get_mapped_df(df, mapping, table):
    df, mapping = get_input_data()
    table = list(TABLE_DICT.keys())
    col_maps = get_table_map(mapping, table[0])col_maps = get_table_map(mapping, table)
    col_maps.head()
    new_df = add_old_data_new_cols(df, col_maps)
    return new_df


# new_df = get_mapped_df(ffpe_db, mapping, 'block_information')


# def add_old_data_new_cols(df, map_df):
#     df_all = pd.DataFrame(df['pk'])
#     for col in map_df['table_tbd']:
#         old_col = get_old_col(map_df, col)
#         df_col = pd.DataFrame(df_all['pk'], columns=['pk'])
#         df_col[old_col] = [None]*len(df)
#         #df_col = df_col.rename(columns={col: old_col})
#         if old_col is not None:
#             df_col[old_col] = df[[old_col]]
#         df_all = pd.merge(df_col, df_all, on='pk')
#         df_all = df_all.rename(columns= {old_col: col})
#     return df_all
