import shutil
import pandas as pd
import os, time
from dateutil import parser

pdf_folder_path = 'D:/Shweta/email/attachments_from_ag'

def get_pdf_file_created_date(pdf_folder_path):
    files = os.listdir(pdf_folder_path)
    dates = []
    for file in files:
        created_date_str = time.ctime(os.path.getctime(os.path.join(pdf_folder_path, file)))
        created_date = parser.parse(created_date_str).date()
        modified_date_str = time.ctime(os.path.getmtime(os.path.join(pdf_folder_path, file)))
        modified_date = parser.parse(modified_date_str).date()
        date_lst = [file, created_date, modified_date]
        dates.append(date_lst)
    df = pd.DataFrame(dates, columns=['file_name', 'file_created_date', 'file_modified_date'])
    return df

df = get_pdf_file_created_date(pdf_folder_path)
df.to_excel('D:/Shweta/email/attachments_from_ag/folder_info_df/2021_09_16_pdf_created_modified_dates_sk.xlsx',
            index=False)

##
# pdf_folder_path = 'D:/Shweta/email/attachments_from_ag'
# report_2021_folder_path = 'D:/Shweta/email/attachments_from_ag/report_of_2021'
# report_2021 = pd.read_excel('D:/Shweta/path_reports/AG_output_df/2021_09_09_bx_cyto_ihc_ki67_data_with_file_txt_sk.xlsx', sheet_name='report_2021')

for report_name in report_2021['report_name']:
    pdf_report_name = report_name[:-6]
    pdf_report_name = pdf_report_name + '.pdf'
    source_path = os.path.join(pdf_folder_path, pdf_report_name)
    destination_path = os.path.join(report_2021_folder_path, pdf_report_name)
    shutil.copy(source_path, destination_path)
    print('done')
