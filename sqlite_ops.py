import os
import sqlite3
import pandas as pd
import numpy as np

folder = 'D:/Shweta/pccm_db'
file = 'PCCM_BreastCancerDB_2021_02_22.db'
# path_db = os.path.join(folder, file)


# conn = sqlite3.connect(path_db)
# cursor = conn.cursor()
# sql_stat = "SELECT * FROM sqlite_master WHERE TYPE = 'table'"
# tables = pd.read_sql(sql_stat, conn)
# tabs = tables['name']
# patient_info = pd.read_sql('SELECT * FROM patient_information_history', conn)


def get_unique_values(folder, file):
    db_path = os.path.join(folder, file)
    conn = sqlite3.connect(db_path)
    sql_stat = "SELECT * FROM sqlite_master WHERE TYPE = 'table'"
    tables = pd.read_sql(sql_stat, conn)
    table_names = tables['name']
    table_idx = [0, 4, 5, 15, 18, 19, 20, 23]

    writer = pd.ExcelWriter('D:/Shweta/pccm_db/output_df/2021_03_17_unique_values_of_db.xlsx',
                            engine='xlsxwriter')
    for table_name in table_names[table_idx]:
        # print(tab)
        tab_stat = 'SELECT * FROM ' + table_name
        get_tab = pd.read_sql(tab_stat, conn)
        # print(get_tab)
        cols = get_tab.columns
        # print(cols)
        unique_value_list = []
        for col in cols:
            col_dat = get_tab[col]
            unique_values = col_dat.unique()
            unique_values_output = np.append(col, unique_values)
            unique_value_list.append(unique_values_output)
            output_df = pd.DataFrame(unique_value_list)
        output_df.to_excel(writer, sheet_name=table_name, index=False)
    writer.save()




# def find_unique_values(df):
#     unique_value_list = []
#     cols = df.columns
#     for col in cols:
#         col_dat = df[col]
#         unique_values = col_dat.unique()
#         unique_values_output = np.append(col, unique_values)
#         unique_value_list.append(unique_values_output)
#         output_df = pd.DataFrame(unique_value_list)
#     return unique_value_list, output_df
#
# unique_value_list, output_df = find_unique_values(patient_info)

