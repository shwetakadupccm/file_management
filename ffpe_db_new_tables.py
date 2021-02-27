import pandas as pd
import numpy as np
import uuid

ffpe_db = pd.read_excel('D:\\Shweta\\Blocks_updated_data\\2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx')
mapping  = pd.read_excel('D:\\Shweta\\Blocks_updated_data\\Final_R_code_excel_files\\2021_02_15_column_names_mapping_sk.xlsx')

def generate_pk(df):
    pks = []
    for i in range(0, len(df)):
        pk = uuid.uuid4().hex
        pks.append(pk)
    return pks


ffpe_db['pk'] = generate_pk(ffpe_db)
cols = ffpe_db.columns.to_list()
cols = cols[-1:] + cols[:-1]
cols

ffpe_db = ffpe_db[cols]

def get_table_map(mapping, table):
    dat = mapping[['old_names', table]]
    filtered_df = dat[dat[table].notnull()]
    filtered_df = filtered_df.rename(columns = {table: 'table_tbd'})
    return filtered_df

filtered_df = get_table_map(mapping,'block_information')

def get_old_col(filtered_df, new_col):
    new_col = (filtered_df[filtered_df.table_tbd == new_col])
    old_col = new_col['old_names'].to_list()[0]
    return old_col

old_col = get_old_col(filtered_df, 'file_number')


def add_old_data_new_cols(df, map_df):
    df_all = pd.DataFrame(df['pk'])
    for col in map_df['table_tbd']:
        old_col = get_old_col(map_df, col)
        df_col = pd.DataFrame(df_all['pk'], columns=['pk'])
        df_col[col] = [None]*len(df)
        #df_col.rename(columns={col: old_col})
        if old_col is not None:
            df_col[old_col] = df[[old_col]]
        df_all = pd.merge(df_col, df_all, on='pk')
        df_all.rename(columns= {old_col: col})
    return df_all


def get_mapped_df(df, mapping, table):
    col_maps = get_table_map(mapping, table)
    new_df = add_old_data_new_cols(df, col_maps)
    return new_df


new_df = get_mapped_df(ffpe_db, mapping, 'block_information')



