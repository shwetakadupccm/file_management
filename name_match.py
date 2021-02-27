import pandas as pd
import re
import fuzzywuzzy

patient_name_mater = pd.read_excel('D://Shweta//Patient_name_matching//2010_2018_names_file_number.xlsx')
ffpe_db = pd.read_excel('D:\\Shweta\\Patient_name_matching\\2021_01_25_PCCM_FFPE_blocks_1_672_RB.xlsx')

# clean the name and make it lower case, removes unnecessary characters

def clean_names(patient_names):
    for name in patient_names:
        # name = name.to_string()
        name = re.sub('[^a-zA-Z]', ' ', name)
        name = name.lower()
        return name


def match(patient_name_master, patient_name_match):
    p1 = clean_names(patient_name_master)
    p2 = clean_names(patient_name_match)
    best_score = 0
    for name in p2:
        score = fuzz.WRatio(name, p1)
        if score > best_score:
            best_score = score
        return p1, name, best_score

match(patient_name_mater['patient_name'] , ffpe_db['patient_name'])

p_master = clean_names(patient_name_mater['patient_name'])
print(p_master)
p_match = clean_names(ffpe_db['Patient Name'])
print(p_match)

for name in p_match:
    if name in p_master:
        print(name)
