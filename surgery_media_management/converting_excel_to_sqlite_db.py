import pandas as pd
import sqlite3
import os

os.getcwd()
## the surgery_media_db is saved in current working directory(D:\\repos\\file_management)
dbname = 'surgery_media_db'
conn = sqlite3.connect(dbname + '.sqlite')

trial_excel = pd.read_excel('D:\\Shweta\\surgery_images_ss\\trial_files_sk\\2021_22_07_trial_file_2021_sx_img_sk_sn.xlsx')

trial_excel.to_sql(name = 'trial_table1', con = conn)

sql_stat = "SELECT * FROM sqlite_master WHERE TYPE = 'table'"
tables = pd.read_sql(sql_stat, conn)

trial_table1 = pd.read_sql('SELECT * FROM trial_table1', conn)

