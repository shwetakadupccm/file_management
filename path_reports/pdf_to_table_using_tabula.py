import pandas as pd
import tabula
import os
import pytesseract as pt
import itertools
import camelot
from PIL import Image

pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
pdf_folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy'
folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_img_txt_files'
output_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_img_txt_files/img_df'
file_name = '06_20_Bx.pdf'
img_name = '06_20_bx_1.jpg'

table_df = tabula.read_pdf(os.path.join(pdf_folder_path, file_name), pages = 'all', multiple_tables=True,
                            stream=True, guess=False, encoding="utf-8")

# tabula.convert_into(os.path.join(pdf_folder_path, file_name), os.path.join(pdf_folder_path, "output.csv"),
#                     output_format="csv", pages='all')

# tables = camelot.read_pdf(os.path.join(pdf_folder_path, file_name), pages='all')
##

def ImagetoXls(path, output_path):
    for imageName in os.listdir(path):
        print(imageName)
        if imageName.endswith('.jpg'):
            inputPath = os.path.join(path, imageName)
            output = os.path.join(output_path, imageName[0:-4] + '.xlsx')
            img = Image.open(inputPath)
            # applying ocr using pytesseract for python
            text = pt.image_to_data(img, output_type='data.frame')
            text = text.dropna()
            lines = text[['line_num']].drop_duplicates()
            #line = 1
            #df = text.loc[text['line_num'] == line]
            #block_nums = df[['block_num']].drop_duplicates().values.tolist()
            #block_nums = list(itertools.chain.from_iterable(block_nums))
            #df_dat = pd.DataFrame(columns=block_nums)
            #df_all = df_dat
            df_all = pd.DataFrame()
            for line in range(0, lines.shape[0]+1):
                df = text.loc[text['line_num'] == line]
                block_nums = df[['block_num']
                                ].drop_duplicates().values.tolist()
                block_nums = list(itertools.chain.from_iterable(block_nums))
                df_dat = pd.DataFrame(columns=block_nums)
                print('line ', line)
                for block in block_nums:
                    dat = df.loc[df['block_num'] == block]
                    dat = dat[['text']].values.tolist()
                    block_data = list(itertools.chain.from_iterable(dat))
                    block_data = ["|".join(block_data)]
                    df_dat[block] = block_data
                df_all = df_all.append(df_dat)
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df_all.to_excel(writer, index=False, na_rep='N/A')
                writer.save()
                writer.close()

ImagetoXls(folder_path, output_path)