import os
import pandas as pd
#read data from text file and convert to df which is printed to excel
def txtToExcel(path, output_path, ncol=7):
    df_all = pd.DataFrame()
    df = pd.DataFrame()
    outputFile = '2020_02_26_Reports_dk.xlsx'
    output = os.path.join(output_path, outputFile)
    for txtFile in os.listdir(path):
        if txtFile.endswith('.txt'):
            print(txtFile)
            filePath = os.path.join(path, txtFile)
            f = open(filePath, 'r')
            fl = f.readlines()
            f.close()
            fl_clean = [item for item in fl if item != '\n']
            entries = len(fl_clean) / ncol
            if entries != int(entries):
                print('this file cannot be converted')
            else:
                df = pd.DataFrame()
                cols = list(range(1, 8))
                for col in cols:
                    col_data = []
                    entry = int(entries * (col - 1))
                    entry_n = int(entries * col)
                    for data in range(entry, entry_n):
                        col_data.append(fl_clean[data])
                    if col == 3:
                        col_1, col_2 = '3_1', '3_2'
                        col_data_2 = [dat.split(' ', maxsplit=1)[1] for dat in col_data]
                        col_data_1 = [dat.split(' ', maxsplit=1)[0] for dat in col_data]
                        df[col_1] = col_data_1
                        df[col_2] = col_data_2
                    else:
                        df[col] = col_data
                print(df.head())
                df_all = df_all.append(df)
                print(df_all.shape)
                print(df_all.head())
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_all.to_excel(writer, index=False, na_rep='N/A')
    print(outputFile)
    writer.save()
    writer.close()

