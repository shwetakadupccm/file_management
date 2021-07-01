import pandas as pd
import fuzzywuzzy
from fuzzywuzzy import fuzz, process

file_num_dat = pd.read_excel('D:\\data_to_dr_pooja\\20210604_Data TILs_all DB.xlsx')
ffpe_data_1_672 = pd.read_excel('D:\\Shweta\\Blocks_updated_data\\2021_01_25_PCCM_FFPE_1_672.xlsx')
ffpe_data_673_1050 = pd.read_excel('D:\\Shweta\\Blocks_updated_data\\2021_06_01_FFPE database_Block Sr. no. 673 to 1050_Danish.xlsx')

dat = ffpe_data_1_672[(ffpe_data_1_672['File_Number'] == '201/17')]

dat_df = []
for file_number in file_num_dat.file_number:
    print(file_number)
    dat = ffpe_data_1_672[(ffpe_data_1_672['File_Number'] == file_number)]
    print(dat)
    dat_df.append(dat)

indexes = []
for index, file_number in enumerate(file_num_dat.file_number):
    print(file_number)
    matched_file_num = process.extractOne(query=file_number, choices=ffpe_data_1_672.File_Number, score_cutoff=100)
    print(matched_file_num)
    indexes.append(matched_file_num[0])

indexes1 = []
for index, file_number in enumerate(file_num_dat.file_number):
    print(file_number)
    matched_file_num = process.extractOne(query=file_number, choices=ffpe_data_673_1050.File_Number, score_cutoff=100)
    print(matched_file_num)
    if matched_file_num is not None:
        indexes1.append(matched_file_num[0])