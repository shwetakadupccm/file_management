import os
import pandas as pd

def make_hyperlink(path, file_name):
    url = "{}"
    return '=HYPERLINK("%s", "%s")' % (url.format(path), file_name)

def get_pdf_path_and_convert_it_to_hyperlink(folder_path):
    pdf_info_lst = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            hyperlink = make_hyperlink(file_path, file)
            lst = [file, hyperlink]
            pdf_info_lst.append(lst)
    df = pd.DataFrame(pdf_info_lst, columns=['file_name', 'hyperlink'])
    return df

df = get_pdf_path_and_convert_it_to_hyperlink('Z:/Clinical_Database/Digitized_Files/Histopath/all_AG_reports_year_wise')

df.to_excel('Z:/Clinical_Database/Digitized_Files/Histopath/all_AG_reports_year_wise/2022_03_04_AG_report_info_with_hyperlink_sk.xlsx',
            index=False)
