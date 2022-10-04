import numpy as np
import pandas as pd
import time, datetime
from preprocessing import *

class Processing:
    def __init__(self, csv):
        self.df = pd.read_csv(csv, dtype=str)  # Open and read csv file
        self.csv = csv
        self.headers = self.df.columns.to_numpy()
        self.area = self.df.to_numpy()  # Process as numpy array

    def save(self):
        df = pd.DataFrame(self.area, columns=self.headers)
        df.to_csv("PROCESSED/" + self.csv, index=False)

    def combine_addr_info(self):
        for row in self.area:
            st_num = str(row[9])
            direct = str(row[10])
            st_nam = str(row[11])
            unit_n = str(row[12])
            city = str(row[13])
            state = str(row[14])
            zipco = str(row[15])
            county = str(row[16])

            if isnan(direct):
                if isnan(unit_n):
                    full_addr = st_num + " " + st_nam + " " + city + " " + state + " " + zipco + " " + county
                else:
                    full_addr = st_num + " " + st_nam + " " + unit_n + " " + city + " " + state + " " + zipco + " " + county
            else:
                full_addr = st_num + " " + direct + " " + st_nam + " " + unit_n + " " + city + " " + state + " " + zipco + " " + county

            row[9] = full_addr

        to_remove = [10, 11, 12, 13, 14, 15, 16]
        self.headers[9] = 'FullAddr'

        self.area = np.delete(self.area, to_remove, 1)
        self.headers = np.delete(self.headers, to_remove)

        return self.area

    def dates_to_unix_time(self):
        for row in self.area:
            row[2] = time.mktime(datetime.datetime.strptime(row[2], "%m/%d/%Y").timetuple())
            row[3] = time.mktime(datetime.datetime.strptime(row[3], "%m/%d/%Y %H:%M:%S %p").timetuple())
            row[4] = time.mktime(datetime.datetime.strptime(row[4], "%m/%d/%Y").timetuple())
            row[5] = time.mktime(datetime.datetime.strptime(row[5], "%m/%d/%Y").timetuple())
        return self.area

    def number_from_money(self, string):
        string.replace(',', '')
        string.replace('$', '')
        return string

    def remove_dollar_comma(self):
        for row in self.area:
            row[6] = str(row[6]).replace(',', '')
            row[6] = str(row[6]).replace('$', '')

            row[7] = str(row[7]).replace(',', '')
            row[7] = str(row[7]).replace('$', '')

            row[8] = str(row[8]).replace(',', '')
            row[8] = str(row[8]).replace('$', '')

    def delete_irrelevant_data(self):
        to_remove = [10, 11, 12, 13, 14, 15, 17, 18]

    def yn_to_binary(self):
        for row in self.area:
            if row[19] == 'No':
                row[19] = 0
            elif row[19] == 'Yes':
                row[19] = 1

            if row[20] == 'No':
                row[20] = 0
            elif row[20] == 'Yes':
                row[20] = 1

            if row[21] == 'No':
                row[21] = 0
            elif row[21] == 'Yes':
                if row[22] == 'Annually':
                    row[21] = row[23]
                elif row[22] == 'Monthly':
                    row[21] = row[23] * 12
                elif row[22] == 'OneTime':
                    row[21] = row[23]
                elif row[22] == 'Quarterly':
                    row[21] = row[23] * 4
                elif row[22] == 'SemiAnnually':
                    row[21] = row[23] * 2
                elif row[22] == 'Unknown':
                    row[21] = 0

        to_remove = [22, 23, 24]
        self.area = np.delete(self.area, to_remove, 1)
        self.headers = np.delete(self.headers, to_remove)

    def process(self):
        self.yn_to_binary()
        self.combine_addr_info()
        self.remove_dollar_comma()
        self.dates_to_unix_time()
        self.save()
