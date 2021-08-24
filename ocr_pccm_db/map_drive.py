import os
import datetime
import pandas as pd
from pathlib import Path


def get_remote_location(password, user_name):
    os.system(r"NET USE P: \\192.168.1.4 %s /USER:%s" % (password, user_name))
    os.system(r"NET USE PERISTENT:YES")

class MapDrive:

    def __init__(self, folder_to_map):
        self.source_folder = folder_to_map
        self.folders = os.listdir(self.source_folder)
        self.col_names = ['path', 'file_name', 'file_size_Mb', 'last_access', 'last_modified', 'created_on']

    # def get_file_names(self, folder):
    #     dat_df = pd.DataFrame(columns=self.col_names)
    #     ch_path = Path(self.source_folder, folder)
    #     if ch_path.is_dir():
    #         for p in ch_path.rglob("*"):
    #             dat_df = self.keep_only_file_name(dat_df, p)
    #     file_name = os.path.join(self.source_folder, str(folder) + '.csv')
    #     dat_df.to_csv(file_name)
    #     return dat_df

    def get_file_names(self, folder):
        dat_df = pd.DataFrame(columns=self.col_names)
        ch_path = Path(self.source_folder, folder)
        if ch_path.is_dir():
            for p in ch_path.rglob("*"):
                print(p)
                try:
                    dat_info = [os.path.split(p)[0], os.path.split(p)[1], (os.path.getsize(p) / 1000),
                                self.convert_date(os.path.getmtime(p)),
                                self.convert_date(os.path.getatime(p)),
                                self.convert_date(os.path.getctime(p))]
                except FileNotFoundError:
                    dat_info = [os.path.split(p)[0], os.path.split(p)[1]] + ['data_not_available', ] * 4
                file_name = os.path.split(p)[1]
                dat_df.loc[file_name] = dat_info
            print(dat_df)
        file_name = os.path.join(self.source_folder, str(folder) + '.csv')
        dat_df.to_csv(file_name)
        return dat_df

    @staticmethod
    def convert_date(timestamp):
        d = datetime.datetime.utcfromtimestamp(timestamp)
        formated_date = d.strftime('%d %b %Y')
        return formated_date

    # def keep_only_file_name(self, dat_df, path_dat):
    #     if not type(path_dat) == 'list':
    #         if os.path.isfile(path_dat):
    #             print(path_dat)
    #             dat_info = [os.path.split(path_dat)[0], os.path.split(path_dat)[1], (os.path.getsize(path_dat) / 1000),
    #                         self.convert_date(os.path.getmtime(path_dat)),
    #                         self.convert_date(os.path.getatime(path_dat)),
    #                         self.convert_date(os.path.getctime(path_dat))]
    #             file_name = os.path.split(path_dat)[1]
    #             dat_df.loc[file_name] = dat_info
    #     print(dat_df)
    #     return dat_df

    def get_file_df(self):
        data_df = [get_dat.get_file_names(folder) for folder in self.folders]
        i = 0
        # try:
        #     iter('list')
        #     is_list = True
        # except TypeError:
        #     is_list = False
        # if is_list:
        for df in data_df:
            i = i + 1
            file_name = str(i) + '.xlsx'
            df.to_excel(file_name)
            file_name = str(i) + '.csv'
            df.to_csv(file_name, sep=',')


if __name__ == '__main__':
    get_remote_location('dknas1999', 'Devaki')
    # source_folder = 'RESEARCH'
    source_folder = 'Prashanti Cancer Care/RESEARCH/RESEARCH-TEAM'
    get_dat = MapDrive(source_folder)
    get_dat.get_file_df()

